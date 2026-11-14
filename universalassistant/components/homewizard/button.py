"""Support for HomeWizard buttons."""

from typing import override

from universalassistant.components.button import ButtonDeviceClass, ButtonEntity
from universalassistant.const import EntityCategory
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HomeWizardConfigEntry, HWEnergyDeviceUpdateCoordinator
from .entity import HomeWizardEntity
from .helpers import homewizard_exception_handler

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: HomeWizardConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Identify button."""
    if entry.runtime_data.data.device.supports_identify():
        async_add_entities([HomeWizardIdentifyButton(entry.runtime_data)])


class HomeWizardIdentifyButton(HomeWizardEntity, ButtonEntity):
    """Representation of a identify button."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = ButtonDeviceClass.IDENTIFY

    def __init__(self, coordinator: HWEnergyDeviceUpdateCoordinator) -> None:
        """Initialize button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.unique_id}_identify"

    @homewizard_exception_handler
    @override
    async def async_press(self) -> None:
        """Identify the device."""
        await self.coordinator.api.identify()
