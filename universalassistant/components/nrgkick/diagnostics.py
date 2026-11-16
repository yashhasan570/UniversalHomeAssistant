"""Diagnostics support for NRGkick."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import UniversalAssistant

from .coordinator import NRGkickConfigEntry

TO_REDACT = {
    "altitude",
    "latitude",
    "longitude",
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    "imei",
    "imsi",
    "ip_address",
    "mac_address",
    "serial",
    "serial_number",
    "ssid",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: NRGkickConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry_data": entry.data,
            "coordinator_data": asdict(entry.runtime_data.data),
        },
        TO_REDACT,
    )
