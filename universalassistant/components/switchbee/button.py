"""Support for SwitchBee scenario button."""

from typing import override

from switchbee.api.central_unit import SwitchBeeError
from switchbee.device import ApiStateCommand, DeviceType

from universalassistant.components.button import ButtonEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import SwitchBeeConfigEntry
from .entity import SwitchBeeEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: SwitchBeeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Switchbee button."""
    coordinator = entry.runtime_data
    async_add_entities(
        SwitchBeeButton(switchbee_device, coordinator)
        for switchbee_device in coordinator.data.values()
        if switchbee_device.type is DeviceType.Scenario
    )


class SwitchBeeButton(SwitchBeeEntity, ButtonEntity):
    """Representation of an Switchbee button."""

    @override
    async def async_press(self) -> None:
        """Fire the scenario in the SwitchBee hub."""
        try:
            await self.coordinator.api.set_state(self._device.id, ApiStateCommand.ON)
        except SwitchBeeError as exp:
            raise __HAC_KEEP__Error(
                f"Failed to fire scenario {self.name}, {exp!s}"
            ) from exp
