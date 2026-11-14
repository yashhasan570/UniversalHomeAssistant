"""Support for Aurora Forecast sensor."""

from typing import override

from universalassistant.components.sensor import SensorEntity, SensorStateClass
from universalassistant.const import PERCENTAGE
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AuroraConfigEntry
from .entity import AuroraEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: AuroraConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    async_add_entities(
        [
            AuroraSensor(
                coordinator=entry.runtime_data,
                translation_key="visibility",
            )
        ]
    )


class AuroraSensor(AuroraEntity, SensorEntity):
    """Implementation of an aurora sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    @override
    def native_value(self) -> int:
        """Return % chance the aurora is visible."""
        return self.coordinator.data
