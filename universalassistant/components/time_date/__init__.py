"""The time_date component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant

from .const import PLATFORMS


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Time & Date from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload Time & Date config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
