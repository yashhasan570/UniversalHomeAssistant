"""Provides diagnostics for Solarlog."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST, CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__

from .coordinator import SolarlogConfigEntry

TO_REDACT = [
    CONF_HOST,
    CONF_PASSWORD,
]


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: SolarlogConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.basic_data_coordinator.data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "solarlog_data": data.to_dict(),
    }
