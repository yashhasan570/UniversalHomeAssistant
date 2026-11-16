"""Diagnostics support for flux_led."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import FluxLedConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: FluxLedConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
        },
        "data": entry.runtime_data.device.diagnostics,
    }
