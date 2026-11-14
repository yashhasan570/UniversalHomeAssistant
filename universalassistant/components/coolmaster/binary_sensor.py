"""Binary Sensor platform for CoolMasterNet integration."""

from typing import override

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import CoolmasterConfigEntry
from .entity import CoolmasterEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: CoolmasterConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the CoolMasterNet binary_sensor platform."""
    coordinator = config_entry.runtime_data
    async_add_entities(
        CoolmasterCleanFilter(coordinator, unit_id) for unit_id in coordinator.data
    )


class CoolmasterCleanFilter(CoolmasterEntity, BinarySensorEntity):
    """Representation of a unit's filter state (true means need to be cleaned)."""

    entity_description = BinarySensorEntityDescription(
        key="clean_filter",
        translation_key="clean_filter",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
    )

    @property
    @override
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._unit.clean_filter
