"""Diagnostics support for OpenWeatherMap."""

from typing import Any

from universalassistant.const import CONF_LANGUAGE, CONF_MODE
from universalassistant.core import __HAC_KEEP__

from . import OpenweathermapConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: OpenweathermapConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.coordinator
    return {
        "mode": entry.options[CONF_MODE],
        "language": entry.options[CONF_LANGUAGE],
        "last_update_success": coordinator.last_update_success,
        "data": coordinator.data,
    }
