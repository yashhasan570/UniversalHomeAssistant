"""Siren support for switch entities."""

from universalassistant.components.siren import (
    DOMAIN as SIREN_DOMAIN,
    SirenEntity,
    SirenEntityFeature,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_ENTITY_ID
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .entity import BaseToggleEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Initialize Siren Switch config entry."""
    registry = er.async_get(hass)
    entity_id = er.async_validate_entity_id(
        registry, config_entry.options[CONF_ENTITY_ID]
    )

    async_add_entities(
        [
            SirenSwitch(
                hass,
                config_entry.title,
                SIREN_DOMAIN,
                entity_id,
                config_entry.entry_id,
            )
        ]
    )


class SirenSwitch(BaseToggleEntity, SirenEntity):
    """Represents a Switch as a Siren."""

    _attr_supported_features = SirenEntityFeature.TURN_ON | SirenEntityFeature.TURN_OFF
