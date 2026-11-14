"""Diagnostics support for PVOutput."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import PvOutputConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: PvOutputConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.data.to_dict()
