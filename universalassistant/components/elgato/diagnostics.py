"""Diagnostics support for Elgato."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import ElgatoConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ElgatoConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "info": coordinator.data.info.to_dict(),
        "state": coordinator.data.state.to_dict(),
    }
