"""__HA_KEEP__ component for accessing the Wallbox Portal API lock."""

from typing import Any, override

from universalassistant.components.lock import LockEntity, LockEntityDescription
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CHARGER_DATA_KEY,
    CHARGER_LOCKED_UNLOCKED_KEY,
    CHARGER_SERIAL_NUMBER_KEY,
)
from .coordinator import WallboxConfigEntry, WallboxCoordinator
from .entity import WallboxEntity

LOCK_TYPES: dict[str, LockEntityDescription] = {
    CHARGER_LOCKED_UNLOCKED_KEY: LockEntityDescription(
        key=CHARGER_LOCKED_UNLOCKED_KEY,
        translation_key="lock",
    ),
}


async def async_setup_entry(
    hass: __HAC_KEEP__,
    entry: WallboxConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create wallbox lock entities in HASS."""
    coordinator: WallboxCoordinator = entry.runtime_data
    async_add_entities(
        WallboxLock(coordinator, description)
        for ent in coordinator.data
        if (description := LOCK_TYPES.get(ent))
    )


# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


class WallboxLock(WallboxEntity, LockEntity):
    """Representation of a wallbox lock."""

    def __init__(
        self,
        coordinator: WallboxCoordinator,
        description: LockEntityDescription,
    ) -> None:
        """Initialize a Wallbox lock."""

        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{description.key}"
            f"-{coordinator.data[CHARGER_DATA_KEY][CHARGER_SERIAL_NUMBER_KEY]}"
        )

    @property
    @override
    def is_locked(self) -> bool:
        """Return the status of the lock."""
        return self.coordinator.data[CHARGER_LOCKED_UNLOCKED_KEY]  # type: ignore[no-any-return]

    @override
    async def async_lock(self, **kwargs: Any) -> None:
        """Lock charger."""
        await self.coordinator.async_set_lock_unlock(True)

    @override
    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock charger."""
        await self.coordinator.async_set_lock_unlock(False)
