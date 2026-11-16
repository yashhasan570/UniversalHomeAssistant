"""Diagnostics support for Overseerr."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from . import CONF_CLOUDHOOK_URL
from .coordinator import OverseerrConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: OverseerrConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    has_cloudhooks = CONF_CLOUDHOOK_URL in entry.data

    data = entry.runtime_data

    return {
        "has_cloudhooks": has_cloudhooks,
        "coordinator_data": asdict(data.data),
    }
