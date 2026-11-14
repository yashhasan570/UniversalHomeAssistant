"""Provides diagnostics for local calendar."""

from typing import Any

from ical.diagnostics import redact_ics

from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util

from . import LocalCalendarConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: LocalCalendarConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    payload: dict[str, Any] = {
        "now": dt_util.now().isoformat(),
        "timezone": str(dt_util.get_default_time_zone()),
        "system_timezone": str(dt_util.naive_now().astimezone().tzinfo),
    }
    store = config_entry.runtime_data
    ics = await store.async_load()
    payload["ics"] = "\n".join(redact_ics(ics))
    return payload
