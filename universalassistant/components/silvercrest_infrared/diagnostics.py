"""Diagnostics platform for the SilverCrest Infrared integration."""

from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return dict(config_entry.data)
