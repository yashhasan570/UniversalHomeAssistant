"""Diagnostics support for Onkyo."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import OnkyoConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: OnkyoConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data
    manager = data.manager

    return {
        "model_name": manager.info.model_name,
        "connected": manager.connected,
        "options": dict(entry.options),
        "channel_muting": {
            channel.value: param.name
            for channel, param in data.channel_muting_coordinator.data.items()
        },
    }
