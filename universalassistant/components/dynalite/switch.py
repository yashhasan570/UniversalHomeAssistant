"""Support for the Dynalite channels and presets as switches."""

from typing import Any, override

from universalassistant.components.switch import SwitchEntity
from universalassistant.const import STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .bridge import DynaliteConfigEntry
from .entity import DynaliteBase, async_setup_entry_base


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: DynaliteConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Record the async_add_entities function to add them later."""
    async_setup_entry_base(
        hass, config_entry, async_add_entities, "switch", DynaliteSwitch
    )


class DynaliteSwitch(DynaliteBase, SwitchEntity):
    """Representation of a Dynalite Channel as a Universal Home Assistant Switch."""

    @property
    @override
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._device.is_on

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._device.async_turn_on()

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._device.async_turn_off()

    @override
    def initialize_state(self, state):
        """Initialize the state from cache."""
        target_level = 1 if state.state == STATE_ON else 0
        self._device.init_level(target_level)
