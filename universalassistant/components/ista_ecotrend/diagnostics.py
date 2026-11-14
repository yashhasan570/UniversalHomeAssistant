"""Diagnostics platform for ista EcoTrend integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import IstaConfigEntry

TO_REDACT = {
    "firstName",
    "lastName",
    "street",
    "houseNumber",
    "documentNumber",
    "postalCode",
    "city",
    "propertyNumber",
    "idAtCustomerUser",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: IstaConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "details": async_redact_data(config_entry.runtime_data.details, TO_REDACT),
        "data": async_redact_data(config_entry.runtime_data.data, TO_REDACT),
    }
