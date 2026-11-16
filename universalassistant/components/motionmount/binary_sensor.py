"""Support for MotionMount binary sensors."""

from typing import override

import motionmount

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from universalassistant.const import EntityCategory
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import MotionMountConfigEntry
from .entity import MotionMountEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: MotionMountConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Vogel's MotionMount from a config entry."""
    mm = entry.runtime_data

    async_add_entities([MotionMountMovingSensor(mm, entry)])


class MotionMountMovingSensor(MotionMountEntity, BinarySensorEntity):
    """The moving sensor of a MotionMount."""

    _attr_device_class = BinarySensorDeviceClass.MOVING
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(
        self, mm: motionmount.MotionMount, config_entry: MotionMountConfigEntry
    ) -> None:
        """Initialize moving binary sensor entity."""
        super().__init__(mm, config_entry)
        self._attr_unique_id = f"{self._base_unique_id}-moving"

    @property
    @override
    def is_on(self) -> bool:
        """Get on status."""
        return self.mm.is_moving or False
