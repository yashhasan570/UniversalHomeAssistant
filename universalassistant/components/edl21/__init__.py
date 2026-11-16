"""The edl21 component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, config_entry: ConfigEntry) -> None:
    """Set up EDL21 integration from a config entry."""
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, config_entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(config_entry, PLATFORMS)
