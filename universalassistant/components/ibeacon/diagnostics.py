"""Diagnostics support for iBeacon Tracker."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import IBeaconConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: IBeaconConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.async_get_diagnostics()
