"""Support for Bond generic devices."""

from typing import Any, override

from aiohttp.client_exceptions import ClientResponseError
from bond_async import Action, DeviceType

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import BondConfigEntry
from .entity import BondEntity


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: BondConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Bond generic devices."""
    data = entry.runtime_data

    async_add_entities(
        BondSwitch(data, device)
        for device in data.hub.devices
        if DeviceType.is_generic(device.type)
    )


class BondSwitch(BondEntity, SwitchEntity):
    """Representation of a Bond generic device."""

    @override
    def _apply_state(self) -> None:
        self._attr_is_on = self._device.state.get("power") == 1

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        await self._bond.action(self._device_id, Action.turn_on())

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        await self._bond.action(self._device_id, Action.turn_off())

    async def async_set_power_belief(self, power_state: bool) -> None:
        """Set switch power belief."""
        try:
            await self._bond.action(
                self._device_id, Action.set_power_state_belief(power_state)
            )
        except ClientResponseError as ex:
            raise UniversalAssistantError(
                "The bond API returned an error calling set_power_state_belief for"
                f" {self.entity_id}.  Code: {ex.status}  Message: {ex.message}"
            ) from ex
