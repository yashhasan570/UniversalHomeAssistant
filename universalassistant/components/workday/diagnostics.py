"""Diagnostics support for Workday."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import WorkdayConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WorkdayConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "config_entry": entry,
    }
