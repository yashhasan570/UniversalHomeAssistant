"""Diagnostics support for Eagle."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .const import CONF_CLOUD_ID, CONF_INSTALL_CODE
from .coordinator import RainforestEagleConfigEntry

TO_REDACT = {CONF_CLOUD_ID, CONF_INSTALL_CODE}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: RainforestEagleConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "data": config_entry.runtime_data.data,
    }
