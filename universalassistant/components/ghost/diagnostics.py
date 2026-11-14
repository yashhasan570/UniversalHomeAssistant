"""Diagnostics support for Ghost."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from . import GhostConfigEntry
from .const import CONF_ADMIN_API_KEY

TO_REDACT = {CONF_ADMIN_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: GhostConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry_data": dict(config_entry.data),
            "coordinator_data": asdict(config_entry.runtime_data.coordinator.data),
        },
        TO_REDACT,
    )
