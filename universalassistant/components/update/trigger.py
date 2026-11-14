"""Provides triggers for update platform."""

from universalassistant.const import STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.trigger import Trigger, make_entity_target_state_trigger

from .const import DOMAIN

TRIGGERS: dict[str, type[Trigger]] = {
    "became_available": make_entity_target_state_trigger(DOMAIN, STATE_ON),
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for update platform."""
    return TRIGGERS
