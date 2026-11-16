"""Diagnostics support for Trafikverket Weatherstation."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from . import TVWeatherConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: TVWeatherConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Trafikverket Weatherstation config entry."""
    return asdict(entry.runtime_data.data)
