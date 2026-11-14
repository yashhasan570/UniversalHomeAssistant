"""Provides conditions for valves."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN, ValveEntityStateAttribute

VALVE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    DOMAIN: DomainSpec(value_source=ValveEntityStateAttribute.IS_CLOSED),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_open": make_entity_state_condition(VALVE_DOMAIN_SPECS, False),
    "is_closed": make_entity_state_condition(VALVE_DOMAIN_SPECS, True),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the valve conditions."""
    return CONDITIONS
