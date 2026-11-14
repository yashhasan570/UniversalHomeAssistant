"""Provides triggers for fans."""

from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.trigger import Trigger, make_entity_target_state_trigger

from .const import DOMAIN

TRIGGERS: dict[str, type[Trigger]] = {
    "turned_off": make_entity_target_state_trigger(DOMAIN, STATE_OFF),
    "turned_on": make_entity_target_state_trigger(DOMAIN, STATE_ON),
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for fans."""
    return TRIGGERS
