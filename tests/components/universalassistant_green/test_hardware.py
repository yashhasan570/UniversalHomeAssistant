"""Test the Universal Universal Home Assistant Green hardware platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, MockModule, mock_integration
from pytest_universalassistant.typing import WebSocketGenerator

from universalassistant.components.hassio import DOMAIN as HASSIO_DOMAIN, HassioNotReadyError
from universalassistant.components.universalassistant_green.const import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_hardware_info(
    hass: UniversalAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """Test we can get the board info."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        return_value={"board": "green"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_green.hardware.get_os_info",
        return_value={"board": "green"},
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {
        "hardware": [
            {
                "board": {
                    "hassio_board_id": "green",
                    "manufacturer": "universalassistant",
                    "model": "green",
                    "revision": None,
                },
                "config_entries": [config_entry.entry_id],
                "dongle": None,
                "name": "Universal Universal Home Assistant Green",
                "url": "https://support.nabucasa.com/hc/en-us/categories/24638797677853-Universal-Assistant-Green",
            }
        ]
    }


@pytest.mark.parametrize("os_info", [{"board": None}, {"board": "other"}])
async def test_hardware_info_fail(
    hass: UniversalAssistant, hass_ws_client: WebSocketGenerator, os_info
) -> None:
    """Test async_info raises if os_info is not as expected."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        return_value={"board": "green"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_green.hardware.get_os_info",
        return_value=os_info,
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {"hardware": []}


async def test_hardware_info_not_ready(
    hass: UniversalAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """Test async_info raises HassioNotReadyError when hassio is not ready."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Universal Universal Home Assistant Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.universalassistant_green.get_os_info",
        return_value={"board": "green"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "universalassistant.components.universalassistant_green.hardware.get_os_info",
        side_effect=HassioNotReadyError,
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {"hardware": []}
