"""Provides conditions for timers."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN, STATUS_ACTIVE, STATUS_IDLE, STATUS_PAUSED

CONDITIONS: dict[str, type[Condition]] = {
    "is_active": make_entity_state_condition(DOMAIN, STATUS_ACTIVE),
    "is_paused": make_entity_state_condition(DOMAIN, STATUS_PAUSED),
    "is_idle": make_entity_state_condition(DOMAIN, STATUS_IDLE),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the timer conditions."""
    return CONDITIONS
