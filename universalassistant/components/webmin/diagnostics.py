"""Diagnostics support for Webmin."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_UNIQUE_ID, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from . import WebminConfigEntry

TO_REDACT = {
    CONF_HOST,
    CONF_UNIQUE_ID,
    CONF_USERNAME,
    CONF_PASSWORD,
    "address",
    "address6",
    "ether",
    "broadcast",
    "device",
    "dir",
    "title",
    "entry_id",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WebminConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {"entry": entry.as_dict(), "data": entry.runtime_data.data}, TO_REDACT
    )
