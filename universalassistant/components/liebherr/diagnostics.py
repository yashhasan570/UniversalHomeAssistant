"""Diagnostics support for Liebherr."""

from dataclasses import asdict
from typing import Any

from universalassistant.const import CONF_API_KEY
from universalassistant.core import __HAC_KEEP__

from .coordinator import LiebherrConfigEntry

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LiebherrConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "devices": {
            device_id: {
                "coordinator": {
                    "last_update_success": coordinator.last_update_success,
                    "update_interval": str(coordinator.update_interval),
                    "last_exception": str(coordinator.last_exception)
                    if coordinator.last_exception
                    else None,
                },
                "data": asdict(coordinator.data),
            }
            for device_id, coordinator in entry.runtime_data.coordinators.items()
        },
    }
