"""Diagnostics support for CPU Speed."""

from typing import Any

from cpuinfo import cpuinfo

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    info: dict[str, Any] = cpuinfo.get_cpu_info()
    return info
