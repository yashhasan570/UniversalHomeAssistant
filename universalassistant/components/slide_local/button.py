"""Support for Slide button."""

from typing import override

from goslideapi.goslideapi import (
    AuthenticationFailed,
    ClientConnectionError,
    ClientTimeoutError,
    DigestAuthCalcError,
)

from universalassistant.components.button import ButtonEntity
from universalassistant.const import EntityCategory
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import SlideConfigEntry, SlideCoordinator
from .entity import SlideEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: SlideConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up button for Slide platform."""

    coordinator = entry.runtime_data

    async_add_entities([SlideButton(coordinator)])


class SlideButton(SlideEntity, ButtonEntity):
    """Defines a Slide button."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_translation_key = "calibrate"

    def __init__(self, coordinator: SlideCoordinator) -> None:
        """Initialize the slide button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data['mac']}-calibrate"

    @override
    async def async_press(self) -> None:
        """Send out a calibrate command."""
        try:
            await self.coordinator.slide.slide_calibrate(self.coordinator.host)
        except (
            ClientConnectionError,
            AuthenticationFailed,
            ClientTimeoutError,
            DigestAuthCalcError,
        ) as ex:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="calibration_error",
            ) from ex
