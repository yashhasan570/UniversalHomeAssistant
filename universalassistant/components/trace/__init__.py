"""Support for script and automation tracing and debugging."""

import logging

import probatio

from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import Event, __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.json import ExtendedJSONEncoder
from universalassistant.helpers.storage import Store
from universalassistant.helpers.typing import ConfigType

from . import websocket_api
from .const import (
    ATTR_ITEM_ID,
    ATTR_RUN_ID,
    CONF_STORED_TRACES,
    DATA_TRACE,
    DATA_TRACE_STORE,
    DEFAULT_STORED_TRACES,
)
from .models import ActionTrace
from .util import async_store_trace

_LOGGER = logging.getLogger(__name__)

DOMAIN = "trace"

STORAGE_KEY = "trace.saved_traces"
STORAGE_VERSION = 1

TRACE_CONFIG_SCHEMA = {
    probatio.Optional(
        CONF_STORED_TRACES, default=DEFAULT_STORED_TRACES
    ): cv.positive_int
}

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = [
    "ATTR_ITEM_ID",
    "ATTR_RUN_ID",
    "CONF_STORED_TRACES",
    "TRACE_CONFIG_SCHEMA",
    "ActionTrace",
    "async_store_trace",
]


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Initialize the trace integration."""
    hass.data[DATA_TRACE] = {}
    websocket_api.async_setup(hass)
    store = Store[dict[str, list]](
        hass, STORAGE_VERSION, STORAGE_KEY, encoder=ExtendedJSONEncoder
    )
    hass.data[DATA_TRACE_STORE] = store

    async def _async_store_traces_at_stop(_: Event) -> None:
        """Save traces to storage."""
        _LOGGER.debug("Storing traces")
        try:
            await store.async_save(
                {
                    key: list(trace_bucket.all_traces())
                    for key, trace_bucket in hass.data[DATA_TRACE].items()
                }
            )
        except __HAC_KEEP__Error as exc:
            _LOGGER.error("Error storing traces", exc_info=exc)

    # Store traces when stopping hass
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_store_traces_at_stop)

    return True
