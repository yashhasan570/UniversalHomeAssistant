"""The dlna_dmr component."""

from universalassistant import config_entries
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .const import LOGGER

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(
    hass: UniversalAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Set up a DLNA DMR device from a config entry."""
    LOGGER.debug("Setting up config entry: %s", entry.unique_id)

    # Forward setup to the appropriate platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, config_entry: config_entries.ConfigEntry
) -> None:
    """Unload a config entry."""
    # Forward to the same platform as async_setup_entry did
    await hass.config_entries.async_unload_platforms_or_raise(config_entry, PLATFORMS)
