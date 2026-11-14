"""Provides diagnostics for Palazzetti."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import PalazzettiConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: PalazzettiConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    client = entry.runtime_data.client

    return {
        "api_data": client.to_dict(redact=True),
    }
