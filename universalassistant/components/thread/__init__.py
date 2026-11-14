"""The Thread integration."""

from universalassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .dataset_store import (
    DatasetAddResult,
    DatasetEntry,
    async_add_dataset,
    async_get_dataset,
    async_get_preferred_dataset,
)
from .websocket_api import async_setup as async_setup_ws_api

__all__ = [
    "DOMAIN",
    "DatasetAddResult",
    "DatasetEntry",
    "async_add_dataset",
    "async_get_dataset",
    "async_get_preferred_dataset",
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the Thread integration."""
    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}
            )
        )
    async_setup_ws_api(hass)
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up a config entry."""


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
