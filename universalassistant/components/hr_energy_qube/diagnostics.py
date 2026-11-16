"""Diagnostics support for Qube Heat Pump."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant

from . import QubeConfigEntry

TO_REDACT = {CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: QubeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "sw_version": coordinator.sw_version,
        "data": asdict(coordinator.data),
    }
