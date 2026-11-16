"""Demo platform that has two fake calendars."""

import datetime as dt
from typing import override

from universalassistant.components.calendar import CalendarEntity, CalendarEvent
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.util import dt as dt_util


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Demo Calendar config entry."""
    async_add_entities(
        [
            DemoCalendar(calendar_data_future(), "Calendar 1"),
            DemoCalendar(calendar_data_current(), "Calendar 2"),
        ]
    )


def calendar_data_future() -> CalendarEvent:
    """Representation of a Demo Calendar for a future event."""
    half_hour_from_now = dt_util.now() + dt.timedelta(minutes=30)
    return CalendarEvent(
        start=half_hour_from_now,
        end=half_hour_from_now + dt.timedelta(minutes=60),
        summary="Future Event",
        description="Future Description",
        location="Future Location",
    )


def calendar_data_current() -> CalendarEvent:
    """Representation of a Demo Calendar for a current event."""
    middle_of_event = dt_util.now() - dt.timedelta(minutes=30)
    return CalendarEvent(
        start=middle_of_event,
        end=middle_of_event + dt.timedelta(minutes=60),
        summary="Current Event",
    )


class DemoCalendar(CalendarEntity):
    """Representation of a Demo Calendar element."""

    def __init__(self, event: CalendarEvent, name: str) -> None:
        """Initialize demo calendar."""
        self._event = event
        self._attr_name = name

    @property
    @override
    def event(self) -> CalendarEvent:
        """Return the next upcoming event."""
        return self._event

    @override
    async def async_get_events(
        self,
        hass: UniversalAssistant,
        start_date: dt.datetime,
        end_date: dt.datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        assert start_date < end_date
        if self._event.start_datetime_local >= end_date:
            return []
        if self._event.end_datetime_local < start_date:
            return []
        return [self._event]
