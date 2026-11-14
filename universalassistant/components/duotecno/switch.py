"""Support for Duotecno switches."""

from typing import Any, override

from duotecno.unit import SwitchUnit

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DuotecnoConfigEntry
from .entity import DuotecnoEntity, api_call


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: DuotecnoConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Velbus switch based on config_entry."""
    async_add_entities(
        DuotecnoSwitch(channel)
        for channel in entry.runtime_data.get_units("SwitchUnit")
    )


class DuotecnoSwitch(DuotecnoEntity, SwitchEntity):
    """Representation of a switch."""

    _unit: SwitchUnit

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._unit.is_on()

    @api_call
    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        await self._unit.turn_on()

    @api_call
    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        await self._unit.turn_off()
