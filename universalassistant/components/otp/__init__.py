"""The One-Time Password (OTP) integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]

__all__ = [
    "DOMAIN",
]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up One-Time Password (OTP) from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
