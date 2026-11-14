"""Describe logbook events."""

from collections.abc import Callable
from typing import Any

from universalassistant.components.logbook import (
    LOGBOOK_ENTRY_CONTEXT_ID,
    LOGBOOK_ENTRY_ENTITY_ID,
    LOGBOOK_ENTRY_ITEM_ID,
    LOGBOOK_ENTRY_MESSAGE,
    LOGBOOK_ENTRY_NAME,
    LOGBOOK_ENTRY_RUN_ID,
    LOGBOOK_ENTRY_SOURCE,
    LazyEventPartialState,
)
from universalassistant.components.trace import ATTR_ITEM_ID, ATTR_RUN_ID
from universalassistant.const import ATTR_ENTITY_ID, ATTR_NAME
from universalassistant.core import __HAC_KEEP__, callback

from .const import ATTR_SOURCE, DOMAIN, EVENT_AUTOMATION_TRIGGERED


@callback
def async_describe_events(
    hass: __HAC_KEEP__,
    async_describe_event: Callable[
        [str, str, Callable[[LazyEventPartialState], dict[str, Any]]], None
    ],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_logbook_event(event: LazyEventPartialState) -> dict[str, Any]:
        """Describe a logbook event."""
        data = event.data
        message = "triggered"
        if ATTR_SOURCE in data:
            message = f"{message} by {data[ATTR_SOURCE]}"

        described: dict[str, Any] = {
            LOGBOOK_ENTRY_NAME: data.get(ATTR_NAME),
            LOGBOOK_ENTRY_MESSAGE: message,
            LOGBOOK_ENTRY_SOURCE: data.get(ATTR_SOURCE),
            LOGBOOK_ENTRY_ENTITY_ID: data.get(ATTR_ENTITY_ID),
            LOGBOOK_ENTRY_CONTEXT_ID: event.context_id,
        }
        if ATTR_ITEM_ID in data and ATTR_RUN_ID in data:
            described[LOGBOOK_ENTRY_ITEM_ID] = data[ATTR_ITEM_ID]
            described[LOGBOOK_ENTRY_RUN_ID] = data[ATTR_RUN_ID]
        return described

    async_describe_event(
        DOMAIN, EVENT_AUTOMATION_TRIGGERED, async_describe_logbook_event
    )
