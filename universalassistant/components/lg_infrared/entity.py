"""Common entity for LG IR integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity import Entity

from .const import DOMAIN


class LgIrEntity(Entity):
    """LG IR base entity providing common device info."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        unique_id_suffix: str,
        device_name: str = "LG TV",
    ) -> None:
        """Initialize LG IR entity."""
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
            manufacturer="LG",
        )
