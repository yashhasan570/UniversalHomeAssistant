"""Diagnostics support for AVM Fritz!Smarthome."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from .coordinator import FritzboxConfigEntry

TO_REDACT = {CONF_USERNAME, CONF_PASSWORD}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: FritzboxConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    diag_data = {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": {},
    }

    entities: dict[str, dict] = {
        **coordinator.data.devices,
        **coordinator.data.templates,
    }
    diag_data["data"] = {
        ain: {k: v for k, v in vars(entity).items() if not k.startswith("_")}
        for ain, entity in entities.items()
    }
    return diag_data
