"""Common entity for Edifier infrared integration."""

from infrared_protocols.codes.edifier.models import EdifierModel

from universalassistant.config_entries import ConfigEntry
from universalassistant.helpers.device_registry import DeviceInfo
from universalassistant.helpers.entity import Entity

from .const import DOMAIN


class EdifierIrEntity(Entity):
    """Edifier IR base entity providing common device info."""

    _attr_has_entity_name = True

    def __init__(
        self, entry: ConfigEntry, model: EdifierModel, unique_id_suffix: str
    ) -> None:
        """Initialize Edifier IR entity."""
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Edifier {model.value}",
            manufacturer="Edifier",
            model=model.value,
        )
