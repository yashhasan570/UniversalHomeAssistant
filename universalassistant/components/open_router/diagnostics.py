"""Diagnostics support for OpenRouter."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_PROMPT
from universalassistant.core import __HAC_KEEP__

from . import OpenRouterConfigEntry

TO_REDACT = {CONF_API_KEY, CONF_PROMPT}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: OpenRouterConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "data": async_redact_data(entry.data, TO_REDACT),
        "subentries": {
            subentry.subentry_id: {
                "title": subentry.title,
                "subentry_type": subentry.subentry_type,
                "data": async_redact_data(subentry.data, TO_REDACT),
            }
            for subentry in entry.subentries.values()
        },
    }
