"""Diagnostics platform for the SilverCrest Infrared integration."""

from typing import Any

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return dict(config_entry.data)
