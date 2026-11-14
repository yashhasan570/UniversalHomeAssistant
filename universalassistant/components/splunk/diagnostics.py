"""Diagnostics support for Splunk."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_TOKEN
from universalassistant.core import UniversalAssistant

from . import DATA_FILTER

TO_REDACT = {CONF_TOKEN}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "entity_filter": hass.data[DATA_FILTER].config,
    }
