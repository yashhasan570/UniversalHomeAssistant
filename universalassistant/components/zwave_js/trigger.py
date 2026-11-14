"""Z-Wave JS trigger dispatcher."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.trigger import Trigger

from .triggers import event, value_updated

TRIGGERS = {
    event.RELATIVE_PLATFORM_TYPE: event.EventTrigger,
    value_updated.RELATIVE_PLATFORM_TYPE: value_updated.ValueUpdatedTrigger,
}


async def async_get_triggers(hass: UniversalAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for Z-Wave JS."""
    return TRIGGERS
