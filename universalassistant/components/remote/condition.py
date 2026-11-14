"""Provides conditions for remotes."""

from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "is_off": make_entity_state_condition(DOMAIN, STATE_OFF),
    "is_on": make_entity_state_condition(DOMAIN, STATE_ON),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the remote conditions."""
    return CONDITIONS
