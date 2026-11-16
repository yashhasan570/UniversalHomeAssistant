"""Support for Nanoleaf buttons."""

from typing import override

from universalassistant.components.button import (
    DOMAIN as BUTTON_DOMAIN,
    ButtonDeviceClass,
    ButtonEntity,
)
from universalassistant.const import EntityCategory
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import NanoleafConfigEntry, NanoleafCoordinator
from .entity import NanoleafEntity, async_handle_nanoleaf_errors


def _identify_unique_id(serial_no: str) -> str:
    """Return the unique ID of the identify button of a device."""
    return f"{serial_no}_identify"


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: NanoleafConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Nanoleaf button."""
    coordinator = entry.runtime_data

    # Devices without an event stream (Nanoleaf Essentials) have no identify
    # endpoint either: the request is answered with HTTP 400 or 404.
    if not coordinator.nanoleaf.supports_events:
        registry = er.async_get(hass)
        unique_id = _identify_unique_id(coordinator.nanoleaf.serial_no)
        # Remove the button that earlier versions created for these devices.
        if entity_id := registry.async_get_entity_id(BUTTON_DOMAIN, DOMAIN, unique_id):
            registry.async_remove(entity_id)
        return

    async_add_entities([NanoleafIdentifyButton(coordinator)])


class NanoleafIdentifyButton(NanoleafEntity, ButtonEntity):
    """Representation of a Nanoleaf identify button."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = ButtonDeviceClass.IDENTIFY

    def __init__(self, coordinator: NanoleafCoordinator) -> None:
        """Initialize the Nanoleaf button."""
        super().__init__(coordinator)
        self._attr_unique_id = _identify_unique_id(self._nanoleaf.serial_no)

    @override
    @async_handle_nanoleaf_errors
    async def async_press(self) -> None:
        """Identify the Nanoleaf."""
        await self._nanoleaf.identify()
