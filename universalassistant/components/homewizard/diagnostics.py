"""Diagnostics support for P1 Monitor."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_IP_ADDRESS
from universalassistant.core import UniversalAssistant

from .coordinator import HomeWizardConfigEntry

TO_REDACT = {
    CONF_IP_ADDRESS,
    "gas_unique_id",
    "id",
    "serial",
    "token",
    "unique_id",
    "unique_meter_id",
    "wifi_ssid",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: HomeWizardConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data.data

    return async_redact_data(
        {
            "entry": async_redact_data(entry.data, TO_REDACT),
            "data": asdict(data),
        },
        TO_REDACT,
    )
