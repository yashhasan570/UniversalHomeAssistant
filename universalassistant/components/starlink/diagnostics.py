"""Fetches diagnostic data for Starlink systems."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import StarlinkConfigEntry

TO_REDACT = {"id", "latitude", "longitude", "altitude"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: StarlinkConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Starlink config entries."""
    return async_redact_data(asdict(config_entry.runtime_data.data), TO_REDACT)
