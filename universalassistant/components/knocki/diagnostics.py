"""Diagnostics support for Knocki."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import KnockiConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: KnockiConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "triggers": [asdict(trigger) for trigger in entry.runtime_data.data.values()],
    }
