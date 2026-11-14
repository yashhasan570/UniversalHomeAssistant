"""Diagnostics support for WMS WebControl pro API integration."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import WebControlProConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WebControlProConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.diag()
