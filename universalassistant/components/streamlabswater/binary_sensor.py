"""Support for Streamlabs Water Monitor Away Mode."""

from typing import override

from universalassistant.components.binary_sensor import BinarySensorEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import StreamlabsConfigEntry, StreamlabsCoordinator
from .entity import StreamlabsWaterEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: StreamlabsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Streamlabs water binary sensor from a config entry."""
    coordinator = entry.runtime_data

    async_add_entities(
        StreamlabsAwayMode(coordinator, location_id) for location_id in coordinator.data
    )


class StreamlabsAwayMode(StreamlabsWaterEntity, BinarySensorEntity):
    """Monitor the away mode state."""

    _attr_translation_key = "away_mode"

    def __init__(self, coordinator: StreamlabsCoordinator, location_id: str) -> None:
        """Initialize the away mode device."""
        super().__init__(coordinator, location_id, "away_mode")

    @property
    @override
    def is_on(self) -> bool:
        """Return if away mode is on."""
        return self.location_data.is_away
