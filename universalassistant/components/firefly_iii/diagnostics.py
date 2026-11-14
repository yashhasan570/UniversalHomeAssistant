"""Diagnostics for the Firefly III integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_URL
from universalassistant.core import __HAC_KEEP__

from .coordinator import FireflyConfigEntry, FireflyDataUpdateCoordinator

TO_REDACT = [CONF_API_KEY, CONF_URL]


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: FireflyConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: FireflyDataUpdateCoordinator = entry.runtime_data

    return {
        "config_entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": {"primary_currency": coordinator.data.primary_currency.to_dict()},
    }
