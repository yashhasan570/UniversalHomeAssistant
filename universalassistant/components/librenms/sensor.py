"""Sensor platform for the LibreNMS integration."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import override

from universalassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.helpers.typing import StateType

from .coordinator import (
    LibrenmsCentralData,
    LibrenmsCentralDataUpdateCoordinator,
    LibrenmsConfigEntry,
)
from .entity import LibrenmsSystemEntity

# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class LibrenmsSystemSensorEntityDescription(SensorEntityDescription):
    """Librenms system sensor entity description."""

    value: Callable[[LibrenmsCentralData], StateType]
    is_suitable: Callable[[LibrenmsCentralData], bool] = lambda _: True


SYSTEM_SENSOR_TYPES: tuple[LibrenmsSystemSensorEntityDescription, ...] = (
    LibrenmsSystemSensorEntityDescription(
        key="device_count",
        translation_key="device_count",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: len(data.devices),
    ),
    LibrenmsSystemSensorEntityDescription(
        key="database_version",
        translation_key="database_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=lambda data: data.system.database_ver,
    ),
    LibrenmsSystemSensorEntityDescription(
        key="netsnmp_version",
        translation_key="netsnmp_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=lambda data: data.system.netsnmp_ver,
    ),
    LibrenmsSystemSensorEntityDescription(
        key="php_version",
        translation_key="php_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=lambda data: data.system.php_ver,
    ),
    LibrenmsSystemSensorEntityDescription(
        key="python_version",
        translation_key="python_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=lambda data: data.system.python_ver,
    ),
    LibrenmsSystemSensorEntityDescription(
        key="rrdtool_version",
        translation_key="rrdtool_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=lambda data: data.system.rrdtool_ver,
    ),
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: LibrenmsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add LibreNMS server state sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        LibrenmsSystemSensorEntity(coordinator, description)
        for description in SYSTEM_SENSOR_TYPES
        if description.is_suitable(coordinator.data)
    )


class LibrenmsSystemSensorEntity(LibrenmsSystemEntity, SensorEntity):
    """Define Librenms sensor entity."""

    entity_description: LibrenmsSystemSensorEntityDescription

    def __init__(
        self,
        coordinator: LibrenmsCentralDataUpdateCoordinator,
        description: LibrenmsSystemSensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"
        self.entity_description = description

    @property
    @override
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        return self.entity_description.value(self.coordinator.data)
