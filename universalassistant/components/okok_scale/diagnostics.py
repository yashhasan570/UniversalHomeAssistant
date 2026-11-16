"""Diagnostics support for the OKOK Scale integration."""

from typing import Any

from universalassistant.components import bluetooth
from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from . import OKOKScaleConfigEntry

SERVICE_INFO_TO_REDACT = frozenset(
    {"address", "advertisement", "device", "name", "source"}
)


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: OKOKScaleConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    address = entry.unique_id
    assert address is not None
    service_info = bluetooth.async_last_service_info(hass, address, connectable=False)
    return {
        "service_info": async_redact_data(
            service_info.as_dict() if service_info else None,
            SERVICE_INFO_TO_REDACT,
        ),
    }
