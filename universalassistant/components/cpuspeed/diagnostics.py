"""Diagnostics support for CPU Speed."""

from typing import Any

from cpuinfo import cpuinfo

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    info: dict[str, Any] = cpuinfo.get_cpu_info()
    return info
