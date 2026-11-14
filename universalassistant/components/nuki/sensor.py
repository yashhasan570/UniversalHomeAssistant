"""Battery sensor for the Nuki Lock."""

from typing import override

from pynuki.device import NukiDevice

from universalassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from universalassistant.const import PERCENTAGE, EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NukiConfigEntry
from .entity import NukiEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: NukiConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Nuki lock sensor."""
    entry_data = entry.runtime_data

    async_add_entities(
        NukiBatterySensor(entry_data.coordinator, lock) for lock in entry_data.locks
    )


class NukiBatterySensor(NukiEntity[NukiDevice], SensorEntity):
    """Representation of a Nuki Lock Battery sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    @override
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"{self._nuki_device.nuki_id}_battery_level"

    @property
    @override
    def native_value(self) -> float:
        """Return the state of the sensor."""
        return self._nuki_device.battery_charge
