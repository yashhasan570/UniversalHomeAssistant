"""Diagnostics support for TRMNL."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import TRMNLConfigEntry

TO_REDACT = {"mac_address"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: TRMNLConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "data": [
            async_redact_data(asdict(device), TO_REDACT)
            for device in entry.runtime_data.data.values()
        ],
    }
