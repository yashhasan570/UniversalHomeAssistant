"""Switch platform for Xthings Cloud."""

from typing import Any, override

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import XthingsCloudConfigEntry
from .entity import XthingsCloudEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: XthingsCloudConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up switch platform."""
    coordinator = entry.runtime_data
    entities = [
        XthingsCloudSwitch(coordinator, device_id, device_data)
        for device_id, device_data in coordinator.data.items()
        if device_data["type"] == "plug"
    ]
    async_add_entities(entities)


class XthingsCloudSwitch(XthingsCloudEntity, SwitchEntity):
    """Xthings Cloud switch entity."""

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.device_data["status"]["on"]

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self.coordinator.client.async_plug_on(self._device_id)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self.coordinator.client.async_plug_off(self._device_id)
