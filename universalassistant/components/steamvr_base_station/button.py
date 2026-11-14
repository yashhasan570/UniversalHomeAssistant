"""Identify button for SteamVR Base Station."""

from typing import override

from universalassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import SteamVRBaseStationConfigEntry
from .entity import SteamVRBaseStationEntity

# Commands to one station are serialized by the library.
PARALLEL_UPDATES = 0

IDENTIFY = ButtonEntityDescription(
    key="identify",
    device_class=ButtonDeviceClass.IDENTIFY,
    entity_category=EntityCategory.DIAGNOSTIC,
)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: SteamVRBaseStationConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the identify button."""
    async_add_entities([SteamVRBaseStationButton(entry.runtime_data, IDENTIFY)])


class SteamVRBaseStationButton(SteamVRBaseStationEntity, ButtonEntity):
    """Blinks the station's LED."""

    @override
    async def async_press(self) -> None:
        """Blink the LED."""
        await self.coordinator.async_identify()
