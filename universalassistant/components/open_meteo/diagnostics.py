"""Diagnostics support for Open-Meteo."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__

from .coordinator import OpenMeteoConfigEntry

TO_REDACT = {
    CONF_LATITUDE,
    CONF_LONGITUDE,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: OpenMeteoConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return async_redact_data(coordinator.data.to_dict(), TO_REDACT)
