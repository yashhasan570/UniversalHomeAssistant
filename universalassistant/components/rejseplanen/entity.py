"""Base entity for Rejseplanen integration."""

import universalassistant.helpers.device_registry as dr
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RejseplanenDataUpdateCoordinator


class RejseplanenEntity(CoordinatorEntity[RejseplanenDataUpdateCoordinator]):
    """Base Rejseplanen entity."""

    _attr_has_entity_name = True
    _attr_attribution = "Data provided by rejseplanen.dk"

    def __init__(
        self,
        coordinator: RejseplanenDataUpdateCoordinator,
        stop_id: int,
        name: str,
        subentry_id: str,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        self._stop_id = stop_id

        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, subentry_id)},
            name=name,
            manufacturer="Rejseplanen",
        )
