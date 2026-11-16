"""Support for Palazzetti buttons."""

from typing import override

from pypalazzetti.exceptions import CommunicationError

from universalassistant.components.button import ButtonEntity
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import PalazzettiConfigEntry, PalazzettiDataUpdateCoordinator
from .entity import PalazzettiEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: PalazzettiConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Palazzetti button platform."""

    coordinator = config_entry.runtime_data
    if coordinator.client.has_fan_silent:
        async_add_entities([PalazzettiSilentButtonEntity(coordinator)])


class PalazzettiSilentButtonEntity(PalazzettiEntity, ButtonEntity):
    """Representation of a Palazzetti Silent button."""

    _attr_translation_key = "silent"

    def __init__(
        self,
        coordinator: PalazzettiDataUpdateCoordinator,
    ) -> None:
        """Initialize a Palazzetti Silent button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.unique_id}-silent"

    @override
    async def async_press(self) -> None:
        """Press the button."""
        try:
            await self.coordinator.client.set_fan_silent()
        except CommunicationError as err:
            raise UniversalAssistantError(
                translation_domain=DOMAIN, translation_key="cannot_connect"
            ) from err

        await self.coordinator.async_request_refresh()
