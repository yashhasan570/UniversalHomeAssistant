"""Provides device automations for control of device."""

import probatio

from universalassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from universalassistant.const import CONF_DEVICE_ID, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.trigger import (
    PluggableAction,
    TriggerActionType,
    TriggerInfo,
)
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, TRIGGER_TYPE_TURN_ON
from .helpers import async_get_turn_on_trigger

TRIGGER_TYPES = {TRIGGER_TYPE_TURN_ON}
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_TYPE): probatio.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: __HAC_KEEP__, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for device."""
    triggers = []
    triggers.append(async_get_turn_on_trigger(device_id))

    return triggers


async def async_attach_trigger(
    hass: __HAC_KEEP__,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    trigger_data = trigger_info["trigger_data"]
    if (trigger_type := config[CONF_TYPE]) == TRIGGER_TYPE_TURN_ON:
        variables = {
            "trigger": {
                **trigger_data,
                "platform": "device",
                "domain": DOMAIN,
                "device_id": config[CONF_DEVICE_ID],
                "description": f"philips_js '{trigger_type}' event",
            }
        }

        turn_on_trigger = async_get_turn_on_trigger(config[CONF_DEVICE_ID])
        return PluggableAction.async_attach_trigger(
            hass, turn_on_trigger, action, variables
        )

    raise __HAC_KEEP__Error(f"Unhandled trigger type {trigger_type}")
