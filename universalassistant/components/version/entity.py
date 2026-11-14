"""Common entity class for Version integration."""

from universalassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from universalassistant.helpers.entity import EntityDescription
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, UNIVERSAL_ASSISTANT
from .coordinator import VersionDataUpdateCoordinator


class VersionEntity(CoordinatorEntity[VersionDataUpdateCoordinator]):
    """Common entity class for Version integration."""

    _attr_device_info = DeviceInfo(
        name=f"{UNIVERSAL_ASSISTANT} {DOMAIN.title()}",
        identifiers={(UNIVERSAL_ASSISTANT, DOMAIN)},
        manufacturer=UNIVERSAL_ASSISTANT,
        entry_type=DeviceEntryType.SERVICE,
    )

    def __init__(
        self,
        coordinator: VersionDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize version entities."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )
