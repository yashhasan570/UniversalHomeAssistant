"""Diagnostics support for Pooldose."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import PooldoseConfigEntry

TO_REDACT = {
    "IP",
    "MAC",
    "WIFI_SSID",
    "AP_SSID",
    "SERIAL_NUMBER",
    "DEVICE_ID",
    "OWNERID",
    "NAME",
    "GROUPNAME",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: PooldoseConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "device_info": async_redact_data(coordinator.device_info, TO_REDACT),
        "data": coordinator.data,
    }
