"""Diagnostics support for LG webOS TV."""

from typing import Any

from aiowebostv import WebOsClient

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_CLIENT_SECRET, CONF_HOST, CONF_UNIQUE_ID
from universalassistant.core import __HAC_KEEP__

from .coordinator import WebOsTvConfigEntry

TO_REDACT = {
    CONF_CLIENT_SECRET,
    CONF_UNIQUE_ID,
    CONF_HOST,
    "device_id",
    "deviceUUID",
    "icon",
    "largeIcon",
    "macAddress",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WebOsTvConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    client: WebOsClient = entry.runtime_data.client

    client_data = {
        "is_registered": client.is_registered(),
        "is_connected": client.is_connected(),
        "tv_info": client.tv_info.__dict__,
        "tv_state": client.tv_state.__dict__,
    }

    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "client": client_data,
        },
        TO_REDACT,
    )
