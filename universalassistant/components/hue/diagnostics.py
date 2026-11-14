"""Diagnostics support for Hue."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .bridge import HueConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: HueConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    bridge = entry.runtime_data
    if bridge.api_version == 1:
        # diagnostics is only implemented for V2 bridges.
        return {}
    # Hue diagnostics are already redacted
    return await bridge.api.get_diagnostics()
