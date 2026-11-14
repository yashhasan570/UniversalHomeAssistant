"""Support for Aurora Forecast binary sensor."""

from typing import override

from universalassistant.components.binary_sensor import BinarySensorEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AuroraConfigEntry
from .entity import AuroraEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: AuroraConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        [
            AuroraSensor(
                coordinator=entry.runtime_data,
                translation_key="visibility_alert",
            )
        ]
    )


class AuroraSensor(AuroraEntity, BinarySensorEntity):
    """Implementation of an aurora sensor."""

    @property
    @override
    def is_on(self) -> bool:
        """Return true if aurora is visible."""
        return self.coordinator.data > self.coordinator.threshold
