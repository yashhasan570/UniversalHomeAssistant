"""Diagnostics support for Devialet."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import DevialetConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: DevialetConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return await entry.runtime_data.client.async_get_diagnostics()
