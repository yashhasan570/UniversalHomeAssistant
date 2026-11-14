"""Diagnostics support for the Eurotronic Comet Blue integration."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_ADDRESS, CONF_PIN, CONF_UNIQUE_ID
from universalassistant.core import UniversalAssistant

from .const import CONF_TITLE
from .coordinator import CometBlueConfigEntry

TO_REDACT = {CONF_ADDRESS, CONF_PIN, CONF_TITLE, CONF_UNIQUE_ID}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: CometBlueConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "coordinator_data": asdict(coordinator.data),
        "raw_data": {str(k): repr(v) for k, v in coordinator.device.raw.items()},
    }
