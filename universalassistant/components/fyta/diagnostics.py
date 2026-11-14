"""Provides diagnostics for Fyta."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from .coordinator import FytaConfigEntry

TO_REDACT = [
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_ACCESS_TOKEN,
]


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: FytaConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "plant_data": {key: value.to_dict() for key, value in data.items()},
    }
