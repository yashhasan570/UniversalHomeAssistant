"""Diagnostics support for Syncthru."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import SyncThruConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: SyncThruConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return entry.runtime_data.data.raw()
