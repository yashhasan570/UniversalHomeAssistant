"""Support for Fluss Devices."""

from typing import override

from fluss_api import FlussApiClientError

from universalassistant.components.button import ButtonEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import FlussConfigEntry
from .entity import FlussEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: FlussConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Fluss Devices, filtering out any invalid payloads."""
    coordinator = entry.runtime_data
    devices = coordinator.data

    async_add_entities(
        FlussButton(coordinator, device_id, device)
        for device_id, device in devices.items()
    )


class FlussButton(FlussEntity, ButtonEntity):
    """Representation of a Fluss button device."""

    _attr_name = None

    @property
    @override
    def available(self) -> bool:
        """Return True only when the device is online."""
        return super().available and self.device["internetConnected"]

    @override
    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self.coordinator.api.async_trigger_device(self.device_id)
        except FlussApiClientError as err:
            raise __HAC_KEEP__Error(f"Failed to trigger device: {err}") from err
