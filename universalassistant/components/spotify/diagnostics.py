"""Diagnostics support for Spotify."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import SpotifyConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: SpotifyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "playback": asdict(entry.runtime_data.coordinator.data),
        "devices": [asdict(dev) for dev in entry.runtime_data.devices.data],
    }
