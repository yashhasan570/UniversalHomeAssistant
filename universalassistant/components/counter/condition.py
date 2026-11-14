"""Provides conditions for counters."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import Condition, make_entity_numerical_condition

DOMAIN = "counter"

CONDITIONS: dict[str, type[Condition]] = {
    "is_value": make_entity_numerical_condition(DOMAIN),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the conditions for counters."""
    return CONDITIONS
