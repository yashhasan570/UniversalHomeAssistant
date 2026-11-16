"""Provides conditions for switches."""

from universalassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN
from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.condition import Condition, make_entity_state_condition

from .const import DOMAIN

SWITCH_DOMAIN_SPECS: dict[str, DomainSpec] = {
    DOMAIN: DomainSpec(),
    INPUT_BOOLEAN_DOMAIN: DomainSpec(),
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_off": make_entity_state_condition(SWITCH_DOMAIN_SPECS, STATE_OFF),
    "is_on": make_entity_state_condition(SWITCH_DOMAIN_SPECS, STATE_ON),
}


async def async_get_conditions(hass: UniversalAssistant) -> dict[str, type[Condition]]:
    """Return the switch conditions."""
    return CONDITIONS
