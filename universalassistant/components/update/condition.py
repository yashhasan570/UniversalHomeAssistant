"""Provides conditions for updates."""

from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_available": make_entity_state_condition(DOMAIN, STATE_ON),
    "is_not_available": make_entity_state_condition(DOMAIN, STATE_OFF),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the update conditions."""
    return CONDITIONS
