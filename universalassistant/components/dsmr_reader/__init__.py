"""The DSMR Reader component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up the DSMR Reader integration."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload the DSMR Reader integration."""
    # no data stored in hass.data
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
