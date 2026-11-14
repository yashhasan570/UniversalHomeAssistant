"""Tests for the Specialized Turbo integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info

from universalassistant.components.bluetooth import BluetoothServiceInfoBleak
from universalassistant.core import __HAC_KEEP__


async def setup_integration(
    hass: __HAC_KEEP__,
    entry: MockConfigEntry,
    service_info: BluetoothServiceInfoBleak,
) -> None:
    """Set up the integration and inject one bike advertisement."""
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    with patch(
        "universalassistant.components.bluetooth.manager.discovery_flow.async_create_flow"
    ):
        inject_bluetooth_service_info(hass, service_info)
    await hass.async_block_till_done()
