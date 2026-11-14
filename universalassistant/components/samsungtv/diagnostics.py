"""Diagnostics support for SamsungTV."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_TOKEN
from universalassistant.core import __HAC_KEEP__

from .const import CONF_SESSION_ID
from .coordinator import SamsungTVConfigEntry

TO_REDACT = {CONF_TOKEN, CONF_SESSION_ID}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: SamsungTVConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "device_info": await coordinator.bridge.async_device_info(),
    }
