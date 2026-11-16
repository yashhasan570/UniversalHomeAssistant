"""Support for AirVisual Pro diagnostics."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD
from universalassistant.core import UniversalAssistant

from .coordinator import AirVisualProConfigEntry

CONF_MAC_ADDRESS = "mac_address"
CONF_SERIAL_NUMBER = "serial_number"

TO_REDACT = {
    CONF_MAC_ADDRESS,
    CONF_PASSWORD,
    CONF_SERIAL_NUMBER,
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: AirVisualProConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": entry.runtime_data.coordinator.data,
        },
        TO_REDACT,
    )
