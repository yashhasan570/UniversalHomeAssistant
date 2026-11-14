"""Support for Balboa switches."""

from typing import Any, override

from pybalboa import SpaClient

from universalassistant.components.switch import SwitchEntity
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import BalboaConfigEntry
from .entity import BalboaEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: BalboaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the spa's switches."""
    spa = entry.runtime_data
    async_add_entities([BalboaSwitchEntity(spa)])


class BalboaSwitchEntity(BalboaEntity, SwitchEntity):
    """Representation of a Balboa switch entity."""

    def __init__(self, spa: SpaClient) -> None:
        """Initialize a Balboa switch entity."""
        super().__init__(spa, "filter_cycle_2_enabled")
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_translation_key = "filter_cycle_2_enabled"

    @property
    @override
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._client.filter_cycle_2_enabled

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._client.configure_filter_cycle(2, enabled=True)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._client.configure_filter_cycle(2, enabled=False)
