"""Diagnostics support for Syncthru."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import SyncThruConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: SyncThruConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return entry.runtime_data.data.raw()
