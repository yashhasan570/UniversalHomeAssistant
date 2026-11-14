"""Diagnostics support for the Pi-hole integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY
from universalassistant.core import __HAC_KEEP__

from .coordinator import PiHoleConfigEntry

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: PiHoleConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    api = entry.runtime_data.api

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": api.data,
        "versions": api.versions,
    }
