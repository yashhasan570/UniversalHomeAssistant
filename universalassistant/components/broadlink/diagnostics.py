"""Diagnostics support for Broadlink."""

from typing import TYPE_CHECKING, Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_TIMEOUT
from universalassistant.core import __HAC_KEEP__

from .const import BROADLINK_DATA


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    device = hass.data[BROADLINK_DATA].devices[entry.entry_id]
    api = device.api
    update_manager = device.update_manager
    if TYPE_CHECKING:
        assert update_manager is not None
    return {
        "device": {
            "type": api.type,
            "devtype": api.devtype,
            "model": api.model,
            "manufacturer": api.manufacturer,
            "fw_version": device.fw_version,
            "timeout": entry.data[CONF_TIMEOUT],
            "is_locked": api.is_locked,
        },
        "available": device.available,
        "update_manager": type(update_manager).__name__,
        "data": update_manager.coordinator.data,
    }
