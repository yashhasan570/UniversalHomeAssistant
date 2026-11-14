"""Support for Abode Security System covers."""

from typing import Any, override

from jaraco.abode.devices.cover import Cover

from universalassistant.components.cover import CoverEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AbodeConfigEntry
from .entity import AbodeDevice


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: AbodeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Abode cover devices."""
    data = entry.runtime_data

    async_add_entities(
        AbodeCover(data, device)
        for device in data.abode.get_devices(generic_type="cover")
    )


class AbodeCover(AbodeDevice, CoverEntity):
    """Representation of an Abode cover."""

    _device: Cover
    _attr_name = None

    @property
    @override
    def is_closed(self) -> bool:
        """Return true if cover is closed, else False."""
        return not self._device.is_open

    @override
    def close_cover(self, **kwargs: Any) -> None:
        """Issue close command to cover."""
        self._device.close_cover()

    @override
    def open_cover(self, **kwargs: Any) -> None:
        """Issue open command to cover."""
        self._device.open_cover()
