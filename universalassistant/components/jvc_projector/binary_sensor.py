"""Binary Sensor platform for JVC Projector integration."""

from typing import override

from jvcprojector import command as cmd

from universalassistant.components.binary_sensor import BinarySensorEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import JVCConfigEntry, JvcProjectorDataUpdateCoordinator
from .entity import JvcProjectorEntity

ON_STATUS = (cmd.Power.ON, cmd.Power.WARMING)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: JVCConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the JVC Projector platform from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([JvcBinarySensor(coordinator)])


class JvcBinarySensor(JvcProjectorEntity, BinarySensorEntity):
    """The entity class for JVC Projector Binary Sensor."""

    _attr_translation_key = "power"

    def __init__(
        self,
        coordinator: JvcProjectorDataUpdateCoordinator,
    ) -> None:
        """Initialize the JVC Projector sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.unique_id}_power"

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the JVC Projector is on."""
        return self.coordinator.data[cmd.Power.name] in ON_STATUS
