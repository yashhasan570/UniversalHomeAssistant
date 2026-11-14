"""Diagnostics support for Nord Pool."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import NordPoolConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: NordPoolConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Nord Pool config entry."""
    return {"raw": entry.runtime_data.data.raw}
