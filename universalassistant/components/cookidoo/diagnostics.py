"""Diagnostics for the Cookidoo integration."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_TOKEN
from universalassistant.core import UniversalAssistant

from .coordinator import CookidooConfigEntry

TO_REDACT = [
    CONF_PASSWORD,
    CONF_TOKEN,
]


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: CookidooConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": asdict(entry.runtime_data.data),
        "user": asdict(entry.runtime_data.user),
    }
