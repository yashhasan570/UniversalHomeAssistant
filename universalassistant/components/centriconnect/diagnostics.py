"""Diagnostics platform for CentriConnect/MyPropane API integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import CentriConnectConfigEntry

TO_REDACT = {"Latitude", "Longitude", "Altitude"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: CentriConnectConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the provided config entry."""
    coord = entry.runtime_data
    return {
        "device_info": {
            "device_id": coord.device_info.device_id,
            "device_name": coord.device_info.device_name,
            "hardware_version": coord.device_info.hardware_version,
            "lte_version": coord.device_info.lte_version,
        },
        "tank_data": async_redact_data(coord.data.raw_data, TO_REDACT),
    }
