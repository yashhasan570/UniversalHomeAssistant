"""Diagnostics support for the HP Printer integration."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant

from .coordinator import HpPrinterConfigEntry

TO_REDACT = {
    CONF_HOST,
    "friendly_name",
    # Job log entries: the print driver's user and document name.
    "name",
    "printer_id",
    "serial_number",
    "ssid_prefix",
    "supply_serial_number",
    "unique_id",
    "user_id",
    "uuid",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: HpPrinterConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "data": async_redact_data(asdict(entry.runtime_data.data), TO_REDACT),
    }
