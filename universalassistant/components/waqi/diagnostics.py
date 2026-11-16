"""Diagnostics support for WAQI."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import WAQIConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: WAQIConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        subentry_id: asdict(coordinator.data)
        for subentry_id, coordinator in entry.runtime_data.items()
    }
