"""Describe universalassistant logbook events."""

from collections.abc import Callable
from typing import Any

from universalassistant.components.logbook import (
    LOGBOOK_ENTRY_ICON,
    LOGBOOK_ENTRY_MESSAGE,
    LOGBOOK_ENTRY_NAME,
)
from universalassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
from universalassistant.core import Event, __HAC_KEEP__, callback
from universalassistant.helpers.typing import NoEventData
from universalassistant.util.event_type import EventType

from .const import DOMAIN

EVENT_TO_NAME: dict[EventType[Any] | str, str] = {
    EVENT_HOMEASSISTANT_STOP: "stopped",
    EVENT_HOMEASSISTANT_START: "started",
}


@callback
def async_describe_events(
    hass: __HAC_KEEP__,
    async_describe_event: Callable[
        [str, EventType[NoEventData] | str, Callable[[Event], dict[str, str]]], None
    ],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_hass_event(event: Event[NoEventData]) -> dict[str, str]:
        """Describe universalassistant logbook event."""
        return {
            LOGBOOK_ENTRY_NAME: "__HA_KEEP__",
            LOGBOOK_ENTRY_MESSAGE: EVENT_TO_NAME[event.event_type],
            LOGBOOK_ENTRY_ICON: "mdi:universal-assistant",
        }

    async_describe_event(DOMAIN, EVENT_HOMEASSISTANT_STOP, async_describe_hass_event)
    async_describe_event(DOMAIN, EVENT_HOMEASSISTANT_START, async_describe_hass_event)
