"""Provides diagnostics for madVR."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__

from .coordinator import MadVRConfigEntry

TO_REDACT = [CONF_HOST]


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: MadVRConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "madvr_data": data,
    }
