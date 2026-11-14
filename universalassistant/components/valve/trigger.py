"""Provides triggers for valves."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import Trigger, make_entity_transition_trigger

from .const import DOMAIN, ValveEntityStateAttribute

VALVE_DOMAIN_SPECS: dict[str, DomainSpec] = {
    DOMAIN: DomainSpec(value_source=ValveEntityStateAttribute.IS_CLOSED),
}


TRIGGERS: dict[str, type[Trigger]] = {
    "closed": make_entity_transition_trigger(
        VALVE_DOMAIN_SPECS, from_states={False}, to_states={True}
    ),
    "opened": make_entity_transition_trigger(
        VALVE_DOMAIN_SPECS, from_states={True}, to_states={False}
    ),
}


async def async_get_triggers(hass: UniversalAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for valves."""
    return TRIGGERS
