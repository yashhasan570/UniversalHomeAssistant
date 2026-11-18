"""NAD Infrared integration for Universal Home Assistant."""

from universalassistant.components.infrared import async_get_emitters
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import entity_registry as er

from .const import CONF_INFRARED_ENTITY_ID, DOMAIN

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up NAD Infrared from a config entry."""
    if er.async_get(hass).async_get(
        entry.data[CONF_INFRARED_ENTITY_ID]
    ) is None and entry.data[CONF_INFRARED_ENTITY_ID] not in async_get_emitters(hass):
        raise ConfigEntryError(
            translation_domain=DOMAIN, translation_key="emitter_not_found"
        )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a NAD Infrared config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
