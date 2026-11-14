"""Diagnostics support for iBeacon Tracker."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import IBeaconConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: IBeaconConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.async_get_diagnostics()
