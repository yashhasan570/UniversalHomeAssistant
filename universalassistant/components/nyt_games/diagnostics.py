"""Diagnostics support for NYT Games."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import NYTGamesConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: NYTGamesConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data.data
    wordle = data.wordle
    return {
        "wordle": {
            **wordle.to_dict(),
            # The library serializes these Wordle fields as date objects
            "last_won": wordle.last_won.isoformat() if wordle.last_won else None,
            "last_completed": (
                wordle.last_completed.isoformat() if wordle.last_completed else None
            ),
        },
        "spelling_bee": data.spelling_bee.to_dict() if data.spelling_bee else None,
        "connections": data.connections.to_dict() if data.connections else None,
    }
