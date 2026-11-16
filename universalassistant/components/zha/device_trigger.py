"""Provides device automations for ZHA devices that emit events."""

import probatio
from zha.application.const import ZHA_EVENT

from universalassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from universalassistant.components.universalassistant.triggers import event as event_trigger
from universalassistant.components.universalassistant.triggers.event import EventTriggerArgument
from universalassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .helpers import async_get_zha_device_proxy, async_is_zha_group_device, get_zha_data

CONF_SUBTYPE = "subtype"
DEVICE = "device"
DEVICE_IEEE = "device_ieee"

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {probatio.Required(CONF_TYPE): str, probatio.Required(CONF_SUBTYPE): str}
)


def _get_device_trigger_data(hass: UniversalAssistant, device_id: str) -> tuple[str, dict]:
    """Get device trigger data for a device, falling back to the cache if possible."""

    # First, try checking to see if the device itself is accessible
    try:
        zha_device = async_get_zha_device_proxy(hass, device_id).device
    except ValueError:
        pass
    else:
        return str(zha_device.ieee), zha_device.device_automation_triggers

    # If not, check the trigger cache but allow any `KeyError`s to propagate
    return get_zha_data(hass).device_trigger_cache[device_id]


async def async_validate_trigger_config(
    hass: UniversalAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    config = TRIGGER_SCHEMA(config)

    # Trigger validation will not occur if the config entry is not loaded
    _, triggers = _get_device_trigger_data(hass, config[CONF_DEVICE_ID])

    trigger = (config[CONF_TYPE], config[CONF_SUBTYPE])
    if trigger not in triggers:
        raise InvalidDeviceAutomationConfig(f"device does not have trigger {trigger}")

    return config


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for state changes based on configuration."""

    try:
        ieee, triggers = _get_device_trigger_data(hass, config[CONF_DEVICE_ID])
    except KeyError as err:
        raise UniversalAssistantError(
            f"Unable to get zha device {config[CONF_DEVICE_ID]}"
        ) from err

    trigger_key: tuple[str, str] = (config[CONF_TYPE], config[CONF_SUBTYPE])

    if trigger_key not in triggers:
        raise UniversalAssistantError(f"Unable to find trigger {trigger_key}")

    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            EventTriggerArgument.PLATFORM: "event",
            EventTriggerArgument.EVENT_TYPE: ZHA_EVENT,
            EventTriggerArgument.EVENT_DATA: {
                DEVICE_IEEE: ieee,
                **triggers[trigger_key],
            },
        }
    )
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )


async def async_get_triggers(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers.

    Make sure the device supports device automations and return the trigger list.
    """
    if async_is_zha_group_device(hass, device_id):
        return []

    try:
        _, triggers = _get_device_trigger_data(hass, device_id)
    except KeyError as err:
        raise InvalidDeviceAutomationConfig from err

    return [
        {
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_PLATFORM: DEVICE,
            CONF_TYPE: trigger,
            CONF_SUBTYPE: subtype,
        }
        for trigger, subtype in triggers
    ]
