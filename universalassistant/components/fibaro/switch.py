"""Support for Fibaro switches."""

from typing import Any, override

from universalassistant.components.switch import SwitchEntity
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import FibaroConfigEntry
from .entity import FibaroEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: FibaroConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Fibaro switches."""
    controller = entry.runtime_data
    async_add_entities(
        [
            FibaroSwitch(device, controller)
            for device in controller.fibaro_devices[Platform.SWITCH]
        ],
        True,
    )


class FibaroSwitch(FibaroEntity, SwitchEntity):
    """Representation of a Fibaro Switch."""

    @override
    def turn_on(self, **kwargs: Any) -> None:
        """Turn device on."""
        self.call_turn_on()
        self._attr_is_on = True

    @override
    def turn_off(self, **kwargs: Any) -> None:
        """Turn device off."""
        self.call_turn_off()
        self._attr_is_on = False

    @override
    def update(self) -> None:
        """Update device state."""
        super().update()
        self._attr_is_on = self.current_binary_state
