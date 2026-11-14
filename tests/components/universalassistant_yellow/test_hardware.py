"""Test the __HA_KEEP__ Yellow hardware platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, MockModule, mock_integration
from pytest_universalassistant.typing import WebSocketGenerator

from universalassistant.components.hassio import DOMAIN as HASSIO_DOMAIN, HassioNotReadyError
from universalassistant.components.universalassistant_yellow.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


@pytest.mark.usefixtures("supervisor_client")
async def test_hardware_info(
    hass: __HAC_KEEP__, hass_ws_client: WebSocketGenerator, addon_store_info
) -> None:
    """Test we can get the board info."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ Yellow",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_yellow.get_os_info",
        return_value={"board": "yellow"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_yellow.hardware.get_os_info",
        return_value={"board": "yellow"},
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {
        "hardware": [
            {
                "board": {
                    "hassio_board_id": "yellow",
                    "manufacturer": "universalassistant",
                    "model": "yellow",
                    "revision": None,
                },
                "config_entries": [config_entry.entry_id],
                "dongle": None,
                "name": "__HA_KEEP__ Yellow",
                "url": "https://support.nabucasa.com/hc/en-us/categories/24734575925149-Universal-Assistant-Yellow",
            }
        ]
    }


@pytest.mark.parametrize("os_info", [{"board": None}, {"board": "other"}])
@pytest.mark.usefixtures("supervisor_client")
async def test_hardware_info_fail(
    hass: __HAC_KEEP__, hass_ws_client: WebSocketGenerator, os_info, addon_store_info
) -> None:
    """Test async_info raises if os_info is not as expected."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ Yellow",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_yellow.get_os_info",
        return_value={"board": "yellow"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_yellow.hardware.get_os_info",
        return_value=os_info,
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {"hardware": []}


@pytest.mark.usefixtures("supervisor_client")
async def test_hardware_info_not_ready(
    hass: __HAC_KEEP__, hass_ws_client: WebSocketGenerator, addon_store_info
) -> None:
    """Test async_info raises HassioNotReadyError when hassio is not ready."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="__HA_KEEP__ Yellow",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_yellow.get_os_info",
        return_value={"board": "yellow"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_yellow.hardware.get_os_info",
        side_effect=HassioNotReadyError,
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {"hardware": []}
