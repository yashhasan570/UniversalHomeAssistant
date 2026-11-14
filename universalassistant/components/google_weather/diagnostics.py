"""Diagnostics support for Google Weather."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__

from .const import CONF_REFERRER
from .coordinator import GoogleWeatherConfigEntry

TO_REDACT = {
    CONF_API_KEY,
    CONF_REFERRER,
    CONF_LATITUDE,
    CONF_LONGITUDE,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: GoogleWeatherConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    diag_data: dict[str, Any] = {
        "entry": entry.as_dict(),
        "subentries": {},
    }

    for subentry_id, subentry_rt in entry.runtime_data.subentries_runtime_data.items():
        diag_data["subentries"][subentry_id] = {
            "observation_data": subentry_rt.coordinator_observation.data.to_dict(),
            "daily_forecast_data": subentry_rt.coordinator_daily_forecast.data.to_dict(),
            "hourly_forecast_data": (
                subentry_rt.coordinator_hourly_forecast.data.to_dict()
            ),
        }

    return async_redact_data(diag_data, TO_REDACT)
