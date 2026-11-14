"""Diagnostics support for BraviaTV."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_MAC, CONF_PIN
from universalassistant.core import UniversalAssistant

from .coordinator import BraviaTVConfigEntry

TO_REDACT = {CONF_MAC, CONF_PIN, "macAddr", "unique_id"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: BraviaTVConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data

    device_info = await coordinator.client.get_system_info()
    command_list = await coordinator.client.get_command_list()

    return {
        "remote_command_list": command_list,
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "device_info": async_redact_data(device_info, TO_REDACT),
    }
