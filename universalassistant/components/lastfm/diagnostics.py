"""Diagnostics support for LastFM."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import LastFMConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LastFMConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "users": [asdict(user_data) for user_data in entry.runtime_data.data.values()],
    }
