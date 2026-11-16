"""Provides device automations for control of LG webOS TV."""

import probatio

from universalassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import ATTR_DEVICE_ID, CONF_DEVICE_ID, CONF_PLATFORM, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.trigger import (
    PluggableAction,
    TriggerActionType,
    TriggerInfo,
)
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .helpers import async_get_device_entry_by_device_id
from .triggers.turn_on import (
    PLATFORM_TYPE as TURN_ON_PLATFORM_TYPE,
    async_get_turn_on_description,
    async_get_turn_on_trigger,
)

TRIGGER_TYPES = {TURN_ON_PLATFORM_TYPE}
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_TYPE): probatio.In(TRIGGER_TYPES),
    }
)


async def async_validate_trigger_config(
    hass: UniversalAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    config = TRIGGER_SCHEMA(config)

    if config[CONF_TYPE] == TURN_ON_PLATFORM_TYPE:
        device_id = config[CONF_DEVICE_ID]
        try:
            device = async_get_device_entry_by_device_id(hass, device_id)
        except ValueError as err:
            raise InvalidDeviceAutomationConfig(
                translation_domain=DOMAIN,
                translation_key="device_not_valid",
                translation_placeholders={"device_id": device_id},
            ) from err

        _, config_entry = dr.async_get_device_and_config_entry_for_domain(
            hass, device.id, domain=DOMAIN
        )
        if config_entry is None:
            raise InvalidDeviceAutomationConfig(
                translation_domain=DOMAIN,
                translation_key="device_not_valid",
                translation_placeholders={"device_id": device.id},
            )
        if config_entry.state is not ConfigEntryState.LOADED:
            raise InvalidDeviceAutomationConfig(
                translation_domain=DOMAIN,
                translation_key="device_config_entry_not_loaded",
                translation_placeholders={"device_id": device.id},
            )

    return config


async def async_get_triggers(
    _hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for device."""
    return [async_get_turn_on_trigger(device_id)]


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    if (trigger_type := config[CONF_TYPE]) == TURN_ON_PLATFORM_TYPE:
        device_id = config[CONF_DEVICE_ID]
        variables = {
            **trigger_info["trigger_data"],
            CONF_PLATFORM: trigger_type,
            ATTR_DEVICE_ID: device_id,
            "description": async_get_turn_on_description(hass, device_id),
        }
        return PluggableAction.async_attach_trigger(
            hass, async_get_turn_on_trigger(device_id), action, {"trigger": variables}
        )

    raise UniversalAssistantError(
        translation_domain=DOMAIN,
        translation_key="unhandled_trigger_type",
        translation_placeholders={"trigger_type": trigger_type},
    )
