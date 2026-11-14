"""Provides triggers for assist satellites."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.trigger import Trigger, make_entity_target_state_trigger

from .const import DOMAIN
from .entity import AssistSatelliteState

TRIGGERS: dict[str, type[Trigger]] = {
    "idle": make_entity_target_state_trigger(DOMAIN, AssistSatelliteState.IDLE),
    "listening": make_entity_target_state_trigger(
        DOMAIN, AssistSatelliteState.LISTENING
    ),
    "processing": make_entity_target_state_trigger(
        DOMAIN, AssistSatelliteState.PROCESSING
    ),
    "responding": make_entity_target_state_trigger(
        DOMAIN, AssistSatelliteState.RESPONDING
    ),
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for assist satellites."""
    return TRIGGERS
