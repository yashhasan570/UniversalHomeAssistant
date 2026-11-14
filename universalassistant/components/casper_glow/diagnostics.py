"""Diagnostics support for the Casper Glow integration."""

from typing import Any

from universalassistant.components import bluetooth
from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import CasperGlowConfigEntry

SERVICE_INFO_TO_REDACT = frozenset({"address", "name", "source", "device"})


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: CasperGlowConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    service_info = bluetooth.async_last_service_info(
        hass, coordinator.device.address, connectable=True
    )

    return {
        "service_info": async_redact_data(
            service_info.as_dict() if service_info else None,
            SERVICE_INFO_TO_REDACT,
        ),
    }
