"""Sensors for Yale Alarm."""

from typing import cast, override

from universalassistant.components.sensor import SensorDeviceClass, SensorEntity
from universalassistant.const import UnitOfTemperature
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.helpers.typing import StateType

from . import YaleConfigEntry
from .entity import YaleEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: YaleConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Yale sensor entry."""

    coordinator = entry.runtime_data

    async_add_entities(
        YaleTemperatureSensor(coordinator, data)
        for data in coordinator.data["temp_sensors"]
    )


class YaleTemperatureSensor(YaleEntity, SensorEntity):
    """Representation of a Yale temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    @override
    def native_value(self) -> StateType:
        "Return native value."
        return cast(float, self.coordinator.data["temp_map"][self._attr_unique_id])
