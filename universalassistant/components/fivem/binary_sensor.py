"""The FiveM binary sensor platform."""

from dataclasses import dataclass
from typing import override

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import NAME_STATUS
from .coordinator import FiveMConfigEntry
from .entity import FiveMEntity, FiveMEntityDescription


@dataclass(frozen=True)
class FiveMBinarySensorEntityDescription(
    BinarySensorEntityDescription, FiveMEntityDescription
):
    """Describes FiveM binary sensor entity."""


BINARY_SENSORS: tuple[FiveMBinarySensorEntityDescription, ...] = (
    FiveMBinarySensorEntityDescription(
        key=NAME_STATUS,
        translation_key="status",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: FiveMConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the FiveM binary sensor platform."""
    coordinator = entry.runtime_data

    async_add_entities(
        [FiveMSensorEntity(coordinator, description) for description in BINARY_SENSORS]
    )


class FiveMSensorEntity(FiveMEntity, BinarySensorEntity):
    """Representation of a FiveM sensor base entity."""

    entity_description: FiveMBinarySensorEntityDescription

    @property
    @override
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.coordinator.data[self.entity_description.key]
