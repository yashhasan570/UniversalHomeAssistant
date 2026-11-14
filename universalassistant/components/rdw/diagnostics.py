"""Diagnostics support for RDW."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import RDWConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: RDWConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data: dict[str, Any] = entry.runtime_data.data.to_dict()
    return data
