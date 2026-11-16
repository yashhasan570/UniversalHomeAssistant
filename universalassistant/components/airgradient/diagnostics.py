"""Diagnostics support for Airgradient."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import AirGradientConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: AirGradientConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return asdict(entry.runtime_data.data)
