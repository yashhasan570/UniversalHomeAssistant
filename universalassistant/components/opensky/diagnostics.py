"""Diagnostics support for OpenSky."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import UniversalAssistant

from .coordinator import OpenSkyConfigEntry

TO_REDACT = {CONF_PASSWORD, CONF_USERNAME}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: OpenSkyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "options": async_redact_data(entry.options, TO_REDACT),
        "flights_in_area": entry.runtime_data.data,
    }
