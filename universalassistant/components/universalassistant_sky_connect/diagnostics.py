"""Diagnostics support for the __HA_KEEP__ SkyConnect integration."""

from typing import Any

from universalassistant.components.universalassistant_hardware.helpers import (
    async_is_firmware_update_in_progress,
)
from universalassistant.components.universalassistant_hardware.util import (
    OwningAddon,
    OwningIntegration,
    guess_hardware_owners,
)
from universalassistant.core import __HAC_KEEP__

from . import __HAC_KEEP__SkyConnectConfigEntry
from .const import DEVICE, FIRMWARE, FIRMWARE_VERSION, MANUFACTURER, PID, PRODUCT, VID


def _owner_as_dict(
    hass: __HAC_KEEP__, owner: OwningAddon | OwningIntegration
) -> dict[str, Any]:
    """Describe a firmware owner without exposing identifiers."""
    if isinstance(owner, OwningAddon):
        return {"addon": owner.slug}
    entry = hass.config_entries.async_get_entry(owner.config_entry_id)
    return {"integration": entry.domain if entry else None}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: __HAC_KEEP__SkyConnectConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    device = entry.data[DEVICE]
    coordinator = entry.runtime_data.coordinator
    owners = await guess_hardware_owners(hass, device)

    return {
        "hardware": {
            "manufacturer": entry.data[MANUFACTURER],
            "product": entry.data[PRODUCT],
            "vid": entry.data[VID],
            "pid": entry.data[PID],
        },
        "firmware": {
            "type": entry.data[FIRMWARE],
            "version": entry.data[FIRMWARE_VERSION],
            "update_in_progress": async_is_firmware_update_in_progress(hass, device),
        },
        "firmware_owners": [
            {
                "source": info.source,
                "firmware_type": info.firmware_type,
                "firmware_version": info.firmware_version,
                "owners": [_owner_as_dict(hass, owner) for owner in info.owners],
            }
            for info in owners
        ],
        "firmware_update_coordinator": {
            "last_update_success": coordinator.last_update_success,
        },
    }
