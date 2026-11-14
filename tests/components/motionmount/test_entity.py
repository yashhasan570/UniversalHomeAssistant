"""Tests for the MotionMount Entity base."""

from unittest.mock import MagicMock

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr, entity_registry as er
from universalassistant.helpers.device_registry import format_mac

from . import ZEROCONF_NAME


async def test_entity_rename(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    mock_motionmount: MagicMock,
) -> None:
    """Tests the state attributes."""
    mock_config_entry.add_to_hass(hass)

    mock_motionmount.is_authenticated = True
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await hass.async_block_till_done()

    mac = format_mac(mock_motionmount.mac.hex())
    device = device_registry.async_get_device_by_connection(
        (dr.CONNECTION_NETWORK_MAC, mac), mock_config_entry.entry_id
    )
    assert device
    assert device.name == ZEROCONF_NAME

    # Simulate the user changed the name of the device
    mock_motionmount.name = "Blub"

    for callback in mock_motionmount.add_listener.call_args_list:
        callback[0][0]()
    await hass.async_block_till_done()

    device = device_registry.async_get_device_by_connection(
        (dr.CONNECTION_NETWORK_MAC, mac), mock_config_entry.entry_id
    )
    assert device
    assert device.name == "Blub"
