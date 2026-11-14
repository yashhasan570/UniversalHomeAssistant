"""WeatherKit sensors."""

from typing import override

from universalassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from universalassistant.const import UnitOfVolumetricFlux
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.helpers.typing import StateType
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_CURRENT_WEATHER
from .coordinator import WeatherKitConfigEntry, WeatherKitDataUpdateCoordinator
from .entity import WeatherKitEntity

SENSORS = (
    SensorEntityDescription(
        key="precipitationIntensity",
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
    ),
    SensorEntityDescription(
        key="pressureTrend",
        device_class=SensorDeviceClass.ENUM,
        options=["rising", "falling", "steady"],
        translation_key="pressure_trend",
    ),
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: WeatherKitConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add sensor entities from a config_entry."""
    coordinator = config_entry.runtime_data

    async_add_entities(
        WeatherKitSensor(coordinator, description) for description in SENSORS
    )


class WeatherKitSensor(
    CoordinatorEntity[WeatherKitDataUpdateCoordinator], WeatherKitEntity, SensorEntity
):
    """WeatherKit sensor entity."""

    def __init__(
        self,
        coordinator: WeatherKitDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        WeatherKitEntity.__init__(
            self, coordinator, unique_id_suffix=entity_description.key
        )
        self.entity_description = entity_description

    @property
    @override
    def native_value(self) -> StateType:
        """Return native value from coordinator current weather."""
        return self.coordinator.data[ATTR_CURRENT_WEATHER][self.entity_description.key]
