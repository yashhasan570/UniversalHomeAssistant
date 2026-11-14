"""Diagnostics support for Zinvolt."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import ZinvoltConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ZinvoltConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "coordinators": [
            {
                coordinator.battery.identifier: asdict(coordinator.data),
            }
            for coordinator in entry.runtime_data.values()
        ],
    }
