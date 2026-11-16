"""Diagnostics support for AccuWeather."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import UniversalAssistant

from .coordinator import AccuWeatherConfigEntry, AccuWeatherData

TO_REDACT = {CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: AccuWeatherConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    accuweather_data: AccuWeatherData = config_entry.runtime_data

    return {
        "config_entry_data": async_redact_data(dict(config_entry.data), TO_REDACT),
        "observation_data": accuweather_data.coordinator_observation.data,
    }
