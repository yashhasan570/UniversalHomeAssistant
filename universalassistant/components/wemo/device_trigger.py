"""Triggers for WeMo devices."""

import probatio
from pywemo.subscribe import EVENT_TYPE_LONG_PRESS

from universalassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from universalassistant.components.universalassistant.triggers import event as event_trigger
from universalassistant.components.universalassistant.triggers.event import EventTriggerArgument
from universalassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, UniversalAssistant
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, WEMO_SUBSCRIPTION_EVENT
from .coordinator import async_get_coordinator

TRIGGER_TYPES = {EVENT_TYPE_LONG_PRESS}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_TYPE): probatio.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """Return a list of triggers."""

    wemo_trigger = {
        # Required fields of TRIGGER_BASE_SCHEMA
        CONF_PLATFORM: "device",
        CONF_DOMAIN: DOMAIN,
        CONF_DEVICE_ID: device_id,
    }

    coordinator = async_get_coordinator(hass, device_id)
    triggers = []

    # Check for long press support.
    if coordinator.supports_long_press:
        triggers.append(
            {
                # Required fields of TRIGGER_SCHEMA
                CONF_TYPE: EVENT_TYPE_LONG_PRESS,
                **wemo_trigger,
            }
        )

    return triggers


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            EventTriggerArgument.PLATFORM: "event",
            EventTriggerArgument.EVENT_TYPE: WEMO_SUBSCRIPTION_EVENT,
            EventTriggerArgument.EVENT_DATA: {
                CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                CONF_TYPE: config[CONF_TYPE],
            },
        }
    )
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )
