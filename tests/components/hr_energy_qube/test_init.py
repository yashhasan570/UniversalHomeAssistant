"""Test the Qube Heat Pump integration init."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.typing import WebSocketGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.hr_energy_qube.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import device_registry as dr

from . import async_shared_connections, setup_integration


@pytest.mark.usefixtures("mock_qube_client")
async def test_setup_and_unload_entry(
    hass: __HAC_KEEP__,
    hass_ws_client: WebSocketGenerator,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup holds a unit on the shared connection and unload releases it."""
    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert await async_shared_connections(hass_ws_client) == [
        (["tcp", "1.2.3.4", 502], {mock_config_entry.entry_id: [1]})
    ]

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
    assert await async_shared_connections(hass_ws_client) == []


@pytest.mark.usefixtures("mock_qube_client")
async def test_device_info(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the device registry entry."""
    await setup_integration(hass, mock_config_entry)

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, mock_config_entry.entry_id), mock_config_entry.entry_id
    )
    assert device == snapshot


async def test_setup_entry_connection_failure(
    hass: __HAC_KEEP__,
    mock_qube_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup failure when the device cannot be reached."""
    mock_qube_client.async_get_software_version.return_value = None
    mock_qube_client.is_connected = False

    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
    assert (
        mock_config_entry.reason == "Unable to connect to the Qube heat pump at 1.2.3.4"
    )


@pytest.mark.usefixtures("mock_qube_client")
async def test_setup_entry_link_settings_in_use(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test setup fails when the device is in use over other link settings."""
    with patch(
        "universalassistant.components.hr_energy_qube.async_get_unit",
        side_effect=__HAC_KEEP__Error("in use"),
    ):
        await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    assert (
        mock_config_entry.reason
        == "The Qube heat pump cannot be set up with these link settings: in use"
    )
