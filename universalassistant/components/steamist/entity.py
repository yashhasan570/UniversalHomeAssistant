"""Support for Steamist sensors."""

from aiosteamist import SteamistStatus

from universalassistant.const import CONF_HOST, CONF_MODEL
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity import Entity, EntityDescription
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import SteamistConfigEntry, SteamistDataUpdateCoordinator


class SteamistEntity(CoordinatorEntity[SteamistDataUpdateCoordinator], Entity):
    """Representation of a Steamist entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SteamistDataUpdateCoordinator,
        entry: SteamistConfigEntry,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        if entry.unique_id:  # Only present if UDP broadcast works
            self._attr_device_info = DeviceInfo(
                connections={(dr.CONNECTION_NETWORK_MAC, entry.unique_id)},
                manufacturer="Steamist",
                model=entry.data[CONF_MODEL],
                configuration_url=f"http://{entry.data[CONF_HOST]}",
            )

    @property
    def _status(self) -> SteamistStatus:
        """Return the steamist status."""
        return self.coordinator.data
