"""Diagnostics support for Environment Canada."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__

from .coordinator import ECConfigEntry

TO_REDACT = {CONF_LATITUDE, CONF_LONGITUDE}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: ECConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "config_entry_data": async_redact_data(dict(config_entry.data), TO_REDACT),
        "weather_data": dict(
            config_entry.runtime_data.weather_coordinator.ec_data.conditions
        ),
    }
