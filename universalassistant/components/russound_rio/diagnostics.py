"""Diagnostics platform for Russound RIO."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import RussoundConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: RussoundConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the provided config entry."""
    return entry.runtime_data.state
