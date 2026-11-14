"""Diagnostics support for Google Assistant SDK."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .helpers import GoogleAssistantSDKConfigEntry

TO_REDACT = {"access_token", "refresh_token"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: GoogleAssistantSDKConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "data": entry.data,
            "options": entry.options,
        },
        TO_REDACT,
    )
