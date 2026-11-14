"""Provides diagnostics for Ohme."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import OhmeConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: OhmeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Ohme."""
    coordinators = config_entry.runtime_data
    client = coordinators.charge_session_coordinator.client

    return {
        "device_info": client.device_info,
        "vehicles": client.vehicles,
        "cap_available": client.cap_available,
    }
