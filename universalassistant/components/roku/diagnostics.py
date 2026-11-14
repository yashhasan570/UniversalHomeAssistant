"""Diagnostics support for Roku."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import RokuConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RokuConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": {
            "data": {
                **entry.data,
            },
            "unique_id": entry.unique_id,
        },
        "data": entry.runtime_data.data.as_dict(),
    }
