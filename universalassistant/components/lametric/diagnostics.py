"""Diagnostics support for LaMetric."""

import json
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import LaMetricConfigEntry

TO_REDACT = {
    "device_id",
    "name",
    "serial_number",
    "ssid",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LaMetricConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    # Round-trip via JSON to trigger serialization
    data = json.loads(coordinator.data.to_json())
    return async_redact_data(data, TO_REDACT)
