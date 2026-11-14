"""Support for the Abode Security System locks."""

from typing import Any, override

from jaraco.abode.devices.lock import Lock

from universalassistant.components.lock import LockEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AbodeConfigEntry
from .entity import AbodeDevice


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: AbodeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Abode lock devices."""
    data = entry.runtime_data

    async_add_entities(
        AbodeLock(data, device)
        for device in data.abode.get_devices(generic_type="lock")
    )


class AbodeLock(AbodeDevice, LockEntity):
    """Representation of an Abode lock."""

    _device: Lock
    _attr_name = None

    @override
    def lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        self._device.lock()

    @override
    def unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        self._device.unlock()

    @property
    @override
    def is_locked(self) -> bool:
        """Return true if device is on."""
        return bool(self._device.is_locked)
