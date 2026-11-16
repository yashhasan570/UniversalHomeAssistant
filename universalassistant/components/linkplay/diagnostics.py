"""Diagnostics support for Linkplay."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import LinkPlayConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: LinkPlayConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data
    return {"device_info": data.bridge.to_dict()}
