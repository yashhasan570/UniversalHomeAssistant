"""Diagnostics support for La Marzocco."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_MAC, CONF_TOKEN
from universalassistant.core import UniversalAssistant

from .const import CONF_USE_BLUETOOTH, TO_REDACT
from .coordinator import LaMarzoccoConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant,
    entry: LaMarzoccoConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.config_coordinator
    device = coordinator.device
    data = {
        "device": device.to_dict(),
        "bluetooth_available": {
            "options_enabled": entry.options.get(CONF_USE_BLUETOOTH, True),
            CONF_MAC: CONF_MAC in entry.data,
            CONF_TOKEN: CONF_TOKEN in entry.data,
        },
    }
    return async_redact_data(data, TO_REDACT)
