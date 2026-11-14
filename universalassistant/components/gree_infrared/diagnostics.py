"""Diagnostics platform for the Gree Infrared integration."""

from dataclasses import asdict
from enum import Enum
from typing import Any

from universalassistant.core import UniversalAssistant

from . import GreeIrConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: GreeIrConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry_data": dict(entry.data),
        "ac_state": {
            key: value.name.lower() if isinstance(value, Enum) else value
            for key, value in asdict(entry.runtime_data.ac_state).items()
        },
    }
