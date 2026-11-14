"""Binary sensor platform for Axle Energy."""

from typing import override

from universalassistant.components.binary_sensor import BinarySensorEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.util import dt as dt_util

from .coordinator import AxleConfigEntry, AxleCoordinator
from .entity import AxleEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: AxleConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the event activity and participation sensors."""
    async_add_entities(
        [
            AxleEventSensor(entry.runtime_data),
            AxleParticipationSensor(entry.runtime_data),
        ]
    )


class AxleEventSensor(AxleEntity, BinarySensorEntity):
    """Indicate whether the household's scheduled event is in progress."""

    _attr_translation_key = "event_in_progress"

    def __init__(self, coordinator: AxleCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_event_in_progress"

    @property
    @override
    def is_on(self) -> bool:
        """Return whether the current time is within the event."""
        if (event := self.coordinator.event) is None:
            return False
        return event.start <= dt_util.utcnow() < event.end


class AxleParticipationSensor(AxleEntity, BinarySensorEntity):
    """Indicate whether the household is opted in."""

    _attr_translation_key = "participation"

    def __init__(self, coordinator: AxleCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_participation"

    @property
    @override
    def is_on(self) -> bool | None:
        """Return unknown when Axle does not supply participation status."""
        if (opted_out := self.coordinator.data.opted_out) is None:
            return None
        return not opted_out
