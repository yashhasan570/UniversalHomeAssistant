"""Helper functions for Samsung TV."""

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import device_registry as dr, entity_registry as er
from universalassistant.helpers.device_registry import DeviceEntry

from .bridge import SamsungTVBridge
from .const import DOMAIN
from .coordinator import SamsungTVConfigEntry


@callback
def async_get_device_entry_by_device_id(
    hass: UniversalAssistant, device_id: str
) -> DeviceEntry:
    """Get Device Entry from Device Registry by device ID.

    Raises ValueError if device ID is invalid.
    """
    device_reg = dr.async_get(hass)
    if (device := device_reg.async_get(device_id, include_child_devices=False)) is None:
        raise ValueError(f"Device {device_id} is not a valid {DOMAIN} device.")

    return device


@callback
def async_get_device_id_from_entity_id(hass: UniversalAssistant, entity_id: str) -> str:
    """Get device ID from an entity ID.

    Raises ValueError if entity or device ID is invalid.
    """
    ent_reg = er.async_get(hass)
    entity_entry = ent_reg.async_get(entity_id)

    if (
        entity_entry is None
        or entity_entry.device_id is None
        or entity_entry.platform != DOMAIN
    ):
        raise ValueError(f"Entity {entity_id} is not a valid {DOMAIN} entity.")

    return entity_entry.device_id


@callback
def async_get_client_by_device_entry(
    hass: UniversalAssistant, device: DeviceEntry
) -> SamsungTVBridge:
    """Get SamsungTVBridge from Device Registry by device entry.

    Raises ValueError if client is not found.
    """
    config_entry: SamsungTVConfigEntry | None
    _, config_entry = dr.async_get_device_and_config_entry_for_domain(
        hass, device.id, domain=DOMAIN
    )
    if config_entry is not None and config_entry.state is ConfigEntryState.LOADED:
        return config_entry.runtime_data.bridge

    raise ValueError(
        f"Device {device.id} is not from an existing {DOMAIN} config entry"
    )
