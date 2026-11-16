"""Diagnostics support for Fast.com."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import FastdotcomConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: FastdotcomConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the config entry."""
    return {"coordinator_data": config_entry.runtime_data.data}
