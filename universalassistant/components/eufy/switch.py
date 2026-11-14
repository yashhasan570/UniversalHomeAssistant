"""Support for EufyHome switches."""

from typing import Any, override

import lakeside

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType


def setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up EufyHome switches."""
    if discovery_info is None:
        return
    add_entities([EufyHomeSwitch(discovery_info)], True)


class EufyHomeSwitch(SwitchEntity):
    """Representation of a EufyHome switch."""

    def __init__(self, device):
        """Initialize the light."""

        self._attr_name = device["name"]
        self._attr_unique_id = device["address"]
        self._switch = lakeside.switch(
            device["address"], device["code"], device["type"]
        )
        self._switch.connect()

    def update(self) -> None:
        """Synchronise state from the switch."""
        self._switch.update()
        self._attr_is_on = self._switch.power

    @override
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the specified switch on."""
        try:
            self._switch.set_state(True)
        except BrokenPipeError:
            self._switch.connect()
            self._switch.set_state(power=True)

    @override
    def turn_off(self, **kwargs: Any) -> None:
        """Turn the specified switch off."""
        try:
            self._switch.set_state(False)
        except BrokenPipeError:
            self._switch.connect()
            self._switch.set_state(False)
