"""Provides device triggers for LG Netcast."""

from typing import Any

import probatio

from universalassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_DEVICE_ID, CONF_PLATFORM, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from . import trigger
from .const import DOMAIN
from .triggers.turn_on import (
    PLATFORM_TYPE as TURN_ON_PLATFORM_TYPE,
    async_get_turn_on_trigger,
)

TRIGGER_TYPES = {TURN_ON_PLATFORM_TYPE}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_TYPE): probatio.In(TRIGGER_TYPES),
    }
)


async def async_validate_trigger_config(
    hass: __HAC_KEEP__, config: ConfigType
) -> ConfigType:
    """Validate config."""
    config = TRIGGER_SCHEMA(config)

    if config[CONF_TYPE] == TURN_ON_PLATFORM_TYPE:
        device_id = config[CONF_DEVICE_ID]

        device, config_entry = dr.async_get_device_and_config_entry_for_domain(
            hass, device_id, domain=DOMAIN
        )
        if device is None:
            raise InvalidDeviceAutomationConfig(
                f"Device {device_id} is not a valid {DOMAIN} device."
            )
        if config_entry is None or config_entry.state is not ConfigEntryState.LOADED:
            raise InvalidDeviceAutomationConfig(
                f"Device {device.id} is not from an existing {DOMAIN} config entry"
            )

    return config


async def async_get_triggers(
    _hass: __HAC_KEEP__, device_id: str
) -> list[dict[str, Any]]:
    """List device triggers for LG Netcast devices."""
    return [async_get_turn_on_trigger(device_id)]


async def async_attach_trigger(
    hass: __HAC_KEEP__,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    if (trigger_type := config[CONF_TYPE]) == TURN_ON_PLATFORM_TYPE:
        trigger_config = {
            CONF_PLATFORM: trigger_type,
            CONF_DEVICE_ID: config[CONF_DEVICE_ID],
        }
        trigger_config = await trigger.async_validate_trigger_config(
            hass, trigger_config
        )
        return await trigger.async_attach_trigger(
            hass, trigger_config, action, trigger_info
        )

    raise __HAC_KEEP__Error(f"Unhandled trigger type {trigger_type}")
