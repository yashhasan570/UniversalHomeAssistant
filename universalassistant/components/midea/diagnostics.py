"""Midea diagnostic."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_MAC, CONF_TOKEN
from universalassistant.core import __HAC_KEEP__

from .const import CONF_KEY, CONF_SN
from .entity import MideaConfigEntry

TO_REDACT = {CONF_TOKEN, CONF_KEY, CONF_MAC, CONF_SN}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: MideaConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    device = entry.runtime_data

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "device_attributes": device.attributes,
    }
