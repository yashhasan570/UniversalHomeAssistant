"""Diagnostics support for Chess.com."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import ChessConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ChessConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "player": asdict(coordinator.data.player),
        "stats": asdict(coordinator.data.stats),
    }
