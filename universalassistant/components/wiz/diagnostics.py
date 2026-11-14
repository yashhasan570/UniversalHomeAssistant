"""Diagnostics support for WiZ."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import WizConfigEntry

TO_REDACT = {"roomId", "homeId"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WizConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
        },
        "data": async_redact_data(entry.runtime_data.bulb.diagnostics, TO_REDACT),
    }
