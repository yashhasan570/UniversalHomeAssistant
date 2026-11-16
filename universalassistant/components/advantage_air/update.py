"""Advantage Air Update platform."""

from typing import override

from universalassistant.components.update import UpdateEntity
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import AdvantageAirCoordinator, AdvantageAirDataConfigEntry
from .entity import AdvantageAirEntity
from .helpers import get_system_id


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: AdvantageAirDataConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AdvantageAir update platform."""

    coordinator = config_entry.runtime_data

    async_add_entities([AdvantageAirApp(coordinator)])


class AdvantageAirApp(AdvantageAirEntity, UpdateEntity):
    """Representation of Advantage Air App."""

    _attr_name = "App"

    def __init__(self, coordinator: AdvantageAirCoordinator) -> None:
        """Initialize the Advantage Air App."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, get_system_id(self.coordinator.data["system"]))},
            manufacturer="Advantage Air",
            model=self.coordinator.data["system"]["sysType"],
            name=self.coordinator.data["system"]["name"],
            sw_version=self.coordinator.data["system"]["myAppRev"],
        )

    @property
    @override
    def installed_version(self) -> str:
        """Return the current app version."""
        return self.coordinator.data["system"]["myAppRev"]

    @property
    @override
    def latest_version(self) -> str:
        """Return if there is an update."""
        if self.coordinator.data["system"]["needsUpdate"]:
            return "Needs Update"
        return self.installed_version
