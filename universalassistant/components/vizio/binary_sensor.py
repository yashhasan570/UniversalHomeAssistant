"""Binary sensor platform for Vizio SmartCast devices."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import override

from vizaio import ChargingStatus

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import VizioConfigEntry, VizioDeviceData
from .entity import VizioDescriptionEntity

PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class VizioBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Vizio binary sensor entity."""

    value_fn: Callable[[VizioDeviceData], bool | None]


BINARY_SENSORS: tuple[VizioBinarySensorEntityDescription, ...] = (
    VizioBinarySensorEntityDescription(
        key="battery_charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        entity_category=EntityCategory.DIAGNOSTIC,
        # A fully charged battery is not drawing charge, so it reports off;
        # the battery level sensor is what tells the user it is full.
        value_fn=lambda data: (
            data.charging_status is ChargingStatus.CHARGING
            if data.charging_status is not None
            else None
        ),
    ),
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: VizioConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Vizio binary sensor entities."""
    coordinator = config_entry.runtime_data.device_coordinator
    if not coordinator.device.profile.has_battery:
        return

    async_add_entities(
        VizioBinarySensor(config_entry, description) for description in BINARY_SENSORS
    )


class VizioBinarySensor(VizioDescriptionEntity, BinarySensorEntity):
    """Binary sensor entity for battery-powered Vizio SmartCast devices."""

    entity_description: VizioBinarySensorEntityDescription

    @property
    @override
    def is_on(self) -> bool | None:
        """Return whether the battery is charging."""
        return self.entity_description.value_fn(self.coordinator.data)
