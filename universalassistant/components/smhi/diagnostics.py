"""Diagnostics support for SMHI."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import UniversalAssistant

from .coordinator import SMHIConfigEntry

TO_REDACT = [
    CONF_LATITUDE,
    CONF_LONGITUDE,
]


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: SMHIConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    runtime_data = entry.runtime_data

    return async_redact_data(
        {
            "entry_data": entry.data,
            "current": runtime_data.coordinator.current,
            "fire_current": runtime_data.fire_coordinator.fire_current,
        },
        TO_REDACT,
    )
