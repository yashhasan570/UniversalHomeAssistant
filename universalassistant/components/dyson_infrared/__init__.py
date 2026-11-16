"""Dyson Infrared integration for Universal Home Assistant."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [Platform.FAN]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Dyson Infrared from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a Dyson Infrared config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
