"""Diagnostics support for Gatus."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import GatusConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: GatusConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "data": [
            {
                "key": ep.key,
                "name": ep.name,
                "group": ep.group,
                "results": [
                    {
                        "success": r.success,
                        "status": r.status,
                    }
                    for r in ep.results
                ],
            }
            for ep in coordinator.data.values()
        ],
    }
