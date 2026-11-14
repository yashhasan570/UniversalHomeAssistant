"""Provides conditions for to-do lists."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import (
    Condition,
    make_entity_numerical_condition,
    make_entity_state_condition,
)

from .const import DOMAIN

CONDITIONS: dict[str, type[Condition]] = {
    "all_completed": make_entity_state_condition(DOMAIN, "0"),
    "incomplete": make_entity_numerical_condition(DOMAIN),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the to-do list conditions."""
    return CONDITIONS
