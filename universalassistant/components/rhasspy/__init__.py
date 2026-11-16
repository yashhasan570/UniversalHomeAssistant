"""The Rhasspy integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up Rhasspy from a config entry."""


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
