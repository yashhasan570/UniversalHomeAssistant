"""Diagnostics support for pegel_online."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import PegelOnlineConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: PegelOnlineConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": entry.as_dict(),
        "data": coordinator.data,
    }
