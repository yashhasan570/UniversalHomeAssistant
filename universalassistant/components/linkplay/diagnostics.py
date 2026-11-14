"""Diagnostics support for Linkplay."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import LinkPlayConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LinkPlayConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data
    return {"device_info": data.bridge.to_dict()}
