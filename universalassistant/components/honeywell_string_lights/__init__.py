"""The Honeywell String Lights integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryError
from universalassistant.helpers import entity_registry as er

from .const import CONF_TRANSMITTER, DOMAIN

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Honeywell String Lights from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_migrate_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Migrate old config entries."""
    if entry.version == 1 and entry.minor_version < 2:
        # Minor version 1 stored the transmitter entity registry UUID.
        transmitter_entity_id = er.async_resolve_entity_id(
            er.async_get(hass), entry.data[CONF_TRANSMITTER]
        )
        if transmitter_entity_id is None:
            raise ConfigEntryError(
                translation_domain=DOMAIN,
                translation_key="transmitter_not_found",
            )
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONF_TRANSMITTER: transmitter_entity_id},
            minor_version=2,
        )
