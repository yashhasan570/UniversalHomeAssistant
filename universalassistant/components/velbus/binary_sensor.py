"""Support for Velbus Binary Sensors."""

from typing import override

from velbusaio.channels import Button as VelbusButton

from universalassistant.components.binary_sensor import BinarySensorEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import VelbusConfigEntry
from .entity import VelbusEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: VelbusConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Velbus switch based on config_entry."""
    await entry.runtime_data.scan_task
    async_add_entities(
        VelbusBinarySensor(channel)
        for channel in entry.runtime_data.controller.get_all_binary_sensor()
    )


class VelbusBinarySensor(VelbusEntity, BinarySensorEntity):
    """Representation of a Velbus Binary Sensor."""

    _channel: VelbusButton

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the sensor is on."""
        return self._channel.is_closed()
