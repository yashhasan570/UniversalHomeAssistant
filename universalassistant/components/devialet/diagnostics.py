"""Diagnostics support for Devialet."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import DevialetConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: DevialetConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return await entry.runtime_data.client.async_get_diagnostics()
