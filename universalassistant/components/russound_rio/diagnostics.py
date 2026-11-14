"""Diagnostics platform for Russound RIO."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import RussoundConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RussoundConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the provided config entry."""
    return entry.runtime_data.state
