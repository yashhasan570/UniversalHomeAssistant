"""Diagnostics support for Knocki."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import KnockiConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: KnockiConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "triggers": [asdict(trigger) for trigger in entry.runtime_data.data.values()],
    }
