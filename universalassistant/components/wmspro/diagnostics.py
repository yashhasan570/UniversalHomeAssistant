"""Diagnostics support for WMS WebControl pro API integration."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import WebControlProConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: WebControlProConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.diag()
