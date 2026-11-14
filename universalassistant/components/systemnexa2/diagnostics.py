"""Diagnostics support for System Nexa 2."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_DEVICE_ID, CONF_HOST
from universalassistant.core import __HAC_KEEP__

from .coordinator import SystemNexa2ConfigEntry

TO_REDACT = {
    CONF_HOST,
    CONF_DEVICE_ID,
    "unique_id",
    "wifi_ssid",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: SystemNexa2ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "device_info": async_redact_data(asdict(coordinator.data.info_data), TO_REDACT),
        "coordinator_available": coordinator.last_update_success,
        "state": coordinator.data.state,
        "settings": {
            name: {
                "name": setting.name,
                "enabled": setting.is_enabled(),
            }
            for name, setting in coordinator.data.on_off_settings.items()
        },
    }
