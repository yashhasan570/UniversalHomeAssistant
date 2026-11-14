"""Diagnostics support for the Mijn Farmad Apotheek integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_EMAIL
from universalassistant.core import __HAC_KEEP__

from . import FarmadConfigEntry
from .const import CONF_REFRESH_TOKEN

TO_REDACT = {CONF_ACCESS_TOKEN, CONF_EMAIL, CONF_REFRESH_TOKEN, "title", "unique_id"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: FarmadConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    diagnostics: dict[str, Any] = {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
    }
    if (data := getattr(entry, "runtime_data", None)) is not None:
        diagnostics["products"] = sorted(
            len(products) for products in data.products.values()
        )
    return diagnostics
