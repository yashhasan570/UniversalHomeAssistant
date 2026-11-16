"""Tests for the Fujitsu HVAC (based on Ayla IOT) integration."""

from ayla_iot_unofficial.fujitsu_hvac import FujitsuHVAC
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant


async def setup_integration(hass: UniversalAssistant, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


def entity_id(device: FujitsuHVAC) -> str:
    """Generate the entity id for the given serial."""
    return f"{Platform.CLIMATE}.{device.device_serial_number}"
