"""Diagnostics support for Stookwijzer."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import StookwijzerConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: StookwijzerConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    client = entry.runtime_data.client
    return {
        "advice": client.advice,
        "air_quality_index": client.lki,
        "windspeed_ms": client.windspeed_ms,
        "forecast": await client.async_get_forecast(),
    }
