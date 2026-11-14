"""Support for Broadlink binary sensors."""

from typing import Any, override

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import BROADLINK_DATA, DOMAINS_AND_TYPES
from .device import BroadlinkDevice
from .entity import BroadlinkEntity


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Broadlink binary sensors."""
    device = hass.data[BROADLINK_DATA].devices[config_entry.entry_id]

    if device.api.type in DOMAINS_AND_TYPES[Platform.BINARY_SENSOR]:
        async_add_entities([BroadlinkThermostatHeating(device)])


class BroadlinkThermostatHeating(BroadlinkEntity, BinarySensorEntity):
    """Representation of the Broadlink thermostat heating output."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_has_entity_name = True
    _attr_translation_key = "heating"

    def __init__(self, device: BroadlinkDevice) -> None:
        """Initialize the binary sensor."""
        super().__init__(device)
        self._attr_unique_id = f"{device.unique_id}-heating"

    @override
    def _update_state(self, data: dict[str, Any]) -> None:
        """Update the state of the entity."""
        self._attr_is_on = bool(data["active"])
