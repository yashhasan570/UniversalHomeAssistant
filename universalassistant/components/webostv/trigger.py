"""LG webOS TV triggers."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.trigger import Trigger

from .triggers.turn_on import TurnOnTrigger

TRIGGERS: dict[str, type[Trigger]] = {
    "turn_on": TurnOnTrigger,
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for LG webOS TV."""
    return TRIGGERS
