"""Diagnostics support for Android TV Remote."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST, CONF_MAC
from universalassistant.core import UniversalAssistant

from .helpers import AndroidTVRemoteConfigEntry

TO_REDACT = {CONF_HOST, CONF_MAC}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: AndroidTVRemoteConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    api = entry.runtime_data
    return async_redact_data(
        {
            "api_device_info": api.device_info,
            "config_entry_data": entry.data,
        },
        TO_REDACT,
    )
