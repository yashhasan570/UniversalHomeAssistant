"""Diagnostics support for air-Q."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD, CONF_UNIQUE_ID
from universalassistant.core import UniversalAssistant

from . import AirQConfigEntry

REDACT_CONFIG = {CONF_PASSWORD, CONF_UNIQUE_ID, CONF_IP_ADDRESS, "title"}
REDACT_DEVICE_INFO = {"identifiers", "name"}
REDACT_COORDINATOR_DATA = {"DeviceID"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: AirQConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "config_entry": async_redact_data(entry.as_dict(), REDACT_CONFIG),
        "device_info": async_redact_data(coordinator.device_info, REDACT_DEVICE_INFO),
        "coordinator_data": async_redact_data(
            coordinator.data, REDACT_COORDINATOR_DATA
        ),
        "options": {
            "clip_negative": coordinator.clip_negative,
            "return_average": coordinator.return_average,
        },
    }
