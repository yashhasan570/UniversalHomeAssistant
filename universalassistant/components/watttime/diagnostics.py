"""Diagnostics support for WattTime."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_PASSWORD,
    CONF_UNIQUE_ID,
    CONF_USERNAME,
)
from universalassistant.core import __HAC_KEEP__

from .const import CONF_BALANCING_AUTHORITY, CONF_BALANCING_AUTHORITY_ABBREV
from .coordinator import WattTimeConfigEntry

CONF_TITLE = "title"

TO_REDACT = {
    CONF_BALANCING_AUTHORITY,
    CONF_BALANCING_AUTHORITY_ABBREV,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_PASSWORD,
    # Config entry title and unique ID may contain sensitive data:
    CONF_TITLE,
    CONF_UNIQUE_ID,
    CONF_USERNAME,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WattTimeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": entry.runtime_data.data,
        },
        TO_REDACT,
    )
