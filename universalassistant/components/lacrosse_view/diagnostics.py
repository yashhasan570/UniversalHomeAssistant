"""Diagnostics support for LaCrosse View."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from .coordinator import LaCrosseConfigEntry

TO_REDACT = {CONF_PASSWORD, CONF_USERNAME}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: LaCrosseConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "coordinator_data": entry.runtime_data.data,
    }
