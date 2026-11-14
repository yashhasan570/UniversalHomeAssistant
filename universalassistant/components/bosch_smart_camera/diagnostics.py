"""Diagnostics support for Bosch Smart Camera."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import BoschCameraConfigEntry

TO_REDACT = {"token", "access_token", "refresh_token", "id", "title"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: BoschCameraConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry_data": dict(entry.data),
            "cameras": [asdict(camera) for camera in entry.runtime_data.data.values()],
        },
        TO_REDACT,
    )
