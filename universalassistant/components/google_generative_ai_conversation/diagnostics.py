"""Diagnostics support for Google Generative AI Conversation."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY
from universalassistant.core import UniversalAssistant

from . import GoogleGenerativeAIConfigEntry

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: GoogleGenerativeAIConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "title": entry.title,
            "data": entry.data,
            "options": entry.options,
            "subentries": dict(entry.subentries),
        },
        TO_REDACT,
    )
