"""Offer Universal Home Assistant core automation rules."""

import probatio

from universalassistant.const import CONF_EVENT, CONF_PLATFORM, EVENT_HOMEASSISTANT_STARTED
from universalassistant.core import CALLBACK_TYPE, Event, HassJob, UniversalAssistant, callback
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from ..const import DOMAIN

EVENT_START = "start"
EVENT_SHUTDOWN = "shutdown"

TRIGGER_SCHEMA = cv.TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_PLATFORM): DOMAIN,
        probatio.Required(CONF_EVENT): probatio.Any(EVENT_START, EVENT_SHUTDOWN),
    }
)


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for events based on configuration."""
    trigger_data = trigger_info["trigger_data"]
    event = config.get(CONF_EVENT)
    job = HassJob(action, f"universalassistant trigger {trigger_info}")

    if event == EVENT_SHUTDOWN:
        return hass.async_add_shutdown_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": DOMAIN,
                    "event": event,
                    "description": "Universal Home Assistant stopping",
                }
            },
        )

    unsub: CALLBACK_TYPE | None = None

    @callback
    def hass_started(_: Event) -> None:
        nonlocal unsub
        unsub = None
        hass.async_run_hass_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": DOMAIN,
                    "event": event,
                    "description": "Universal Home Assistant starting",
                }
            },
        )

    # Only fires if armed before EVENT_HOMEASSISTANT_STARTED; if hass is already
    # started, the trigger doesn't fire.
    unsub = hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, hass_started)

    @callback
    def remove() -> None:
        if unsub is not None:
            unsub()

    return remove
