"""Diagnostics support for TechnoVE."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import TechnoVEConfigEntry

TO_REDACT = {"mac_address", "network_ssid", "unique_id"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: TechnoVEConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(asdict(entry.runtime_data.data.info), TO_REDACT)
