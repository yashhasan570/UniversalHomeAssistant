"""LG IR Remote integration for Universal Universal Home Assistant."""

import logging

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.EVENT,
    Platform.MEDIA_PLAYER,
    Platform.SELECT,
    Platform.SWITCH,
]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up LG IR from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a LG IR config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_migrate_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Migrate old config entry."""
    if entry.version == 1:
        # v1 used the infrared entity_id in the entry's unique_id, which is
        # not stable and was removed in v2.
        _LOGGER.debug("Migrating config entry from version 1 to 2")
        hass.config_entries.async_update_entry(entry, unique_id=None, version=2)
