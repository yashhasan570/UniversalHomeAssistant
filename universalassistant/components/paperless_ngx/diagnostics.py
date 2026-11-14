"""Diagnostics support for Paperless-ngx."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import PaperlessConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    entry: PaperlessConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "pngx_version": entry.runtime_data.status.api.host_version,
        "data": {
            "statistics": asdict(entry.runtime_data.statistics.data),
            "status": asdict(entry.runtime_data.status.data),
        },
    }
