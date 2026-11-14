"""Diagnostics support for Airgradient."""

from dataclasses import asdict
from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import AirGradientConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: AirGradientConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return asdict(entry.runtime_data.data)
