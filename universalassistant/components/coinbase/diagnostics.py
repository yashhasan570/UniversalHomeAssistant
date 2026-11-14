"""Diagnostics support for Coinbase."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_API_KEY, CONF_API_TOKEN, CONF_ID
from universalassistant.core import __HAC_KEEP__

from . import CoinbaseConfigEntry
from .const import API_ACCOUNT_AMOUNT, API_RESOURCE_PATH, CONF_TITLE

TO_REDACT = {
    API_ACCOUNT_AMOUNT,
    API_RESOURCE_PATH,
    CONF_API_KEY,
    CONF_API_TOKEN,
    CONF_ID,
    CONF_TITLE,
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: CoinbaseConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "accounts": entry.runtime_data.accounts,
        },
        TO_REDACT,
    )
