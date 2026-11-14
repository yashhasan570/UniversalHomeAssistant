"""Number platform for the Silla Prism integration."""

from typing import override

from universalassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from universalassistant.const import UnitOfElectricCurrent
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import MAX_CURRENT, MIN_CURRENT, PORT
from .coordinator import PrismConfigEntry, PrismCoordinator
from .entity import PrismEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: PrismConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Prism number entities."""
    async_add_entities([PrismUserCurrentNumber(entry.runtime_data)])


class PrismUserCurrentNumber(PrismEntity, NumberEntity):
    """User-set maximum charging current (mirrors the +/- buttons)."""

    _attr_translation_key = "user_current"
    _attr_device_class = NumberDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_native_min_value = MIN_CURRENT
    _attr_native_max_value = MAX_CURRENT
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator: PrismCoordinator) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, "user_current")

    @property
    @override
    def native_value(self) -> float | None:
        """Return the user-set current reported by Prism, in amps."""
        return self.coordinator.device.status.port(PORT).user_current

    @override
    async def async_set_native_value(self, value: float) -> None:
        """Set the user maximum charging current."""
        await self.coordinator.device.set_current_user(int(value), PORT)
