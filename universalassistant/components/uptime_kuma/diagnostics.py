"""Diagnostics platform for Uptime Kuma."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import UptimeKumaConfigEntry

TO_REDACT = {"monitor_url", "monitor_hostname"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: UptimeKumaConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "version": entry.runtime_data.api.version.version,
        "monitors": async_redact_data(
            {k: asdict(v) for k, v in entry.runtime_data.data.items()}, TO_REDACT
        ),
    }
