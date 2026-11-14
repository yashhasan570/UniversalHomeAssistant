"""Diagnostics support for ReCollect Waste."""

import dataclasses
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_UNIQUE_ID
from universalassistant.core import __HAC_KEEP__

from .const import CONF_PLACE_ID
from .coordinator import RecollectWasteConfigEntry

CONF_AREA_NAME = "area_name"
CONF_TITLE = "title"

TO_REDACT = {
    CONF_AREA_NAME,
    CONF_PLACE_ID,
    # Config entry title and unique ID may contain sensitive data:
    CONF_TITLE,
    CONF_UNIQUE_ID,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RecollectWasteConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": [dataclasses.asdict(event) for event in entry.runtime_data.data],
        },
        TO_REDACT,
    )
