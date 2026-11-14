"""Provides diagnostics for slide_local."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__

from .coordinator import SlideConfigEntry

TO_REDACT = [
    CONF_PASSWORD,
]


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: SlideConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "slide_data": data,
    }
