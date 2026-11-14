"""Diagnostics support for Holiday."""

from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "config_entry": entry,
    }
