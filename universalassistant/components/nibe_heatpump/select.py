"""The Nibe Heat Pump select."""

from typing import override

from nibe.coil import Coil, CoilData

from universalassistant.components.select import ENTITY_ID_FORMAT, SelectEntity
from universalassistant.const import EntityCategory
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import CoilCoordinator, NibeHeatpumpConfigEntry
from .entity import CoilEntity


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: NibeHeatpumpConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up platform."""

    coordinator = config_entry.runtime_data

    async_add_entities(
        Select(coordinator, coil)
        for coil in coordinator.coils
        if coil.is_writable and coil.mappings and not coil.is_boolean
    )


class Select(CoilEntity, SelectEntity):
    """Select entity."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: CoilCoordinator, coil: Coil) -> None:
        """Initialize entity."""
        assert coil.mappings
        super().__init__(coordinator, coil, ENTITY_ID_FORMAT)
        self._attr_options = list(coil.mappings.values())
        self._attr_current_option = None

    @override
    def _async_read_coil(self, data: CoilData) -> None:
        if not isinstance(data.value, str):
            self._attr_current_option = None
            return

        self._attr_current_option = data.value

    @override
    async def async_select_option(self, option: str) -> None:
        """Support writing value."""
        await self._async_write_coil(option)
