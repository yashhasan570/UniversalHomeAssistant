"""Button platform for the Helty Flow integration."""

from typing import override

from pyhelty import HeltyError

from universalassistant.components.button import ButtonEntity
from universalassistant.const import EntityCategory
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import HeltyConfigEntry, HeltyDataUpdateCoordinator
from .entity import HeltyEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: HeltyConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Helty buttons."""
    async_add_entities([HeltyResetFilterButton(entry.runtime_data)])


class HeltyResetFilterButton(HeltyEntity, ButtonEntity):
    """Resets the filter-life counter after the filter has been replaced."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_translation_key = "reset_filter"

    def __init__(self, coordinator: HeltyDataUpdateCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._device_id}_reset_filter"

    @override
    async def async_press(self) -> None:
        """Reset the filter-life counter."""
        try:
            await self.coordinator.client.async_reset_filter()
        except HeltyError as err:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="reset_filter_failed",
            ) from err
        await self.coordinator.async_request_refresh()
