"""Diagnostics support for STIEBEL ELTRON."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant

from .coordinator import StiebelEltronConfigEntry

TO_REDACT = {CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: StiebelEltronConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "model": coordinator.device_info.model,
        "data": {
            "current_temp": coordinator.api_client.get_current_temp(),
            "target_temp": coordinator.api_client.get_target_temp(),
            "current_humidity": coordinator.api_client.get_current_humidity(),
            "operating_mode": coordinator.api_client.get_operation().name,
            "heating_status": coordinator.api_client.get_heating_status(),
            "cooling_status": coordinator.api_client.get_cooling_status(),
            "filter_alarm": coordinator.api_client.get_filter_alarm_status(),
        },
    }
