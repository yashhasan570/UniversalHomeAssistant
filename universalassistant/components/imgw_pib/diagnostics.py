"""Diagnostics support for IMGW-PIB."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import ImgwPibConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: ImgwPibConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.coordinator

    return {
        "config_entry_data": entry.as_dict(),
        "hydrological_data": asdict(coordinator.data),
    }
