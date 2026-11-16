"""Diagnostics support for Homeassistant Analytics."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from . import AnalyticsInsightsConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: AnalyticsInsightsConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "options": dict(entry.options),
        "names": entry.runtime_data.names,
        "data": asdict(entry.runtime_data.coordinator.data),
    }
