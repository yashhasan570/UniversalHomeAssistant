"""Diagnostics support for Ridwell."""

import dataclasses
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_UNIQUE_ID, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from .coordinator import RidwellConfigEntry

CONF_TITLE = "title"

TO_REDACT = {
    CONF_PASSWORD,
    # Config entry title and unique ID may contain sensitive data:
    CONF_TITLE,
    CONF_UNIQUE_ID,
    CONF_USERNAME,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RidwellConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": [
                dataclasses.asdict(event)
                for events in entry.runtime_data.data.values()
                for event in events
            ],
        },
        TO_REDACT,
    )
