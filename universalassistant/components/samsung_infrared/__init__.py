"""Samsung IR Remote integration for Universal Home Assistant."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [Platform.BUTTON, Platform.CLIMATE, Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Samsung IR from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a Samsung IR config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
