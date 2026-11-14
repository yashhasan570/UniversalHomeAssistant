"""Creates LOQED sensors."""

from typing import Final, override

from universalassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from universalassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import LoqedConfigEntry, LoqedDataCoordinator, StatusMessage
from .entity import LoqedEntity

SENSORS: Final[tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        key="ble_strength",
        translation_key="ble_strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="battery_percentage",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=PERCENTAGE,
    ),
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: LoqedConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Loqed lock platform."""
    coordinator = entry.runtime_data

    async_add_entities(LoqedSensor(coordinator, sensor) for sensor in SENSORS)


class LoqedSensor(LoqedEntity, SensorEntity):
    """Representation of Sensor state."""

    def __init__(
        self, coordinator: LoqedDataCoordinator, description: SensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{self.coordinator.lock.id}_{description.key}"

    @property
    def data(self) -> StatusMessage:
        """Return data object from DataUpdateCoordinator."""
        return self.coordinator.lock

    @property
    @override
    def native_value(self) -> int:
        """Return state of sensor."""
        return getattr(self.data, self.entity_description.key)
