"""Diagnostics support for Tile."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_UUID
from universalassistant.core import UniversalAssistant

from .coordinator import TileConfigEntry

CONF_ALTITUDE = "altitude"

TO_REDACT = {
    CONF_ALTITUDE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_UUID,
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: TileConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinators = entry.runtime_data.values()

    return async_redact_data(
        {"tiles": [coordinator.tile.as_dict() for coordinator in coordinators]},
        TO_REDACT,
    )
