"""Diagnostics support for Vistapool."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import UniversalAssistant

from . import VistapoolConfigEntry

TO_REDACT = {
    CONF_PASSWORD,
    CONF_USERNAME,
    "city",
    "lat",
    "lng",
    "street",
    "title",
    "unique_id",
    "wifi",
    "zipcode",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant,
    entry: VistapoolConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a Vistapool config entry."""
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "pools": [
            async_redact_data(coordinator.data, TO_REDACT)
            for coordinator in entry.runtime_data.coordinators.values()
        ],
    }
