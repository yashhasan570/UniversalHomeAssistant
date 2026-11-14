"""Diagnostics support for RDW."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import RDWConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RDWConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data: dict[str, Any] = entry.runtime_data.data.to_dict()
    return data
