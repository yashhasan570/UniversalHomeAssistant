"""Diagnostics support for Airly."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_UNIQUE_ID,
)
from universalassistant.core import __HAC_KEEP__

from .coordinator import AirlyConfigEntry

TO_REDACT = {CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_UNIQUE_ID}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: AirlyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "coordinator_data": coordinator.data,
    }
