"""Provides conditions for calendars."""

from universalassistant.const import STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_event_active": make_entity_state_condition(DOMAIN, STATE_ON),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the calendar conditions."""
    return CONDITIONS
