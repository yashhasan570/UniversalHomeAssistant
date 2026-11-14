"""Entity representing a Goal Zero Yeti device."""

from typing import override

from goalzero import Yeti

from universalassistant.const import CONF_NAME
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity import EntityDescription
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, MANUFACTURER
from .coordinator import GoalZeroDataUpdateCoordinator


class GoalZeroEntity(CoordinatorEntity[GoalZeroDataUpdateCoordinator]):
    """Representation of a Goal Zero Yeti entity."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoalZeroDataUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize a Goal Zero Yeti entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}/{description.key}"

    @property
    @override
    def device_info(self) -> DeviceInfo:
        """Return the device information of the entity."""
        return DeviceInfo(
            connections={(dr.CONNECTION_NETWORK_MAC, self._api.sysdata["macAddress"])},
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=self._api.sysdata["model"],
            name=self.coordinator.config_entry.data[CONF_NAME].capitalize(),
            sw_version=self._api.data["firmwareVersion"],
        )

    @property
    def _api(self) -> Yeti:
        """Return api from coordinator."""
        return self.coordinator.api
