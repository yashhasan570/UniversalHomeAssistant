"""Diagnostics support for immich."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_HOST
from universalassistant.core import __HAC_KEEP__

from .coordinator import ImmichConfigEntry

TO_REDACT = {CONF_API_KEY, CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ImmichConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": asdict(coordinator.data),
    }
