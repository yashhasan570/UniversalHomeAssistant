"""Create device without entities."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from .const import DOMAIN


def async_create_device(
    hass: __HAC_KEEP__,
    config_entry_id: str,
    device_name: str | None,
    device_translation_key: str | None,
    device_translation_placeholders: dict[str, str] | None,
    unique_id: str,
    via_device_id: str | None = None,
) -> dr.DeviceEntry:
    """Create a device."""
    device_registry = dr.async_get(hass)
    return device_registry.async_get_or_create(
        config_entry_id=config_entry_id,
        identifiers={(DOMAIN, unique_id)},
        name=device_name,
        translation_key=device_translation_key,
        translation_placeholders=device_translation_placeholders,
        via_device_id=via_device_id,
    )
