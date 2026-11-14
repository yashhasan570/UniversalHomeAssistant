"""Diagnostics support for OneDrive."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_TOKEN
from universalassistant.core import __HAC_KEEP__

from .coordinator import OneDriveConfigEntry

TO_REDACT = {"display_name", "email", CONF_ACCESS_TOKEN, CONF_TOKEN}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    entry: OneDriveConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    coordinator = entry.runtime_data.coordinator

    data = {
        "drive": asdict(coordinator.data),
        "config": {
            **entry.data,
            **entry.options,
        },
    }

    return async_redact_data(data, TO_REDACT)
