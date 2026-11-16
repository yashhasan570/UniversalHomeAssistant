"""Support for Velux switches."""

from typing import Any, override

from pyvlx import OnOffSwitch

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import VeluxConfigEntry
from .entity import VeluxEntity, wrap_pyvlx_call_exceptions

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: VeluxConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up switch(es) for Velux platform."""
    pyvlx = config_entry.runtime_data.pyvlx
    async_add_entities(
        VeluxOnOffSwitch(hass, node, config_entry.entry_id)
        for node in pyvlx.nodes
        if isinstance(node, OnOffSwitch)
    )


class VeluxOnOffSwitch(VeluxEntity, SwitchEntity):
    """Representation of a Velux on/off switch."""

    _attr_name = None

    node: OnOffSwitch

    @property
    @override
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.node.is_on()

    @wrap_pyvlx_call_exceptions
    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.node.set_on()

    @wrap_pyvlx_call_exceptions
    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.node.set_off()
