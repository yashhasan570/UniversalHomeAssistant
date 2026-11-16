"""Diagnostics support for PVOutput."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import PvOutputConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: PvOutputConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.data.to_dict()
