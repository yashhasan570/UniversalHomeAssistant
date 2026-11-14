"""Provides conditions for counters."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.condition import Condition, make_entity_numerical_condition

DOMAIN = "counter"

CONDITIONS: dict[str, type[Condition]] = {
    "is_value": make_entity_numerical_condition(DOMAIN),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the conditions for counters."""
    return CONDITIONS
