"""Diagnostics support for Sensor.Community."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__

from .const import CONF_SENSOR_ID
from .coordinator import LuftdatenConfigEntry

TO_REDACT = {
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SENSOR_ID,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LuftdatenConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return async_redact_data(coordinator.data, TO_REDACT)
