"""Diagnostics support for Plugwise."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import PlugwiseConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: PlugwiseConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return coordinator.data
