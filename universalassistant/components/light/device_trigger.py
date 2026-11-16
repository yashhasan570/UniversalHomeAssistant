"""Provides device trigger for lights."""

import probatio

from universalassistant.components.device_automation import toggle_entity
from universalassistant.const import CONF_DOMAIN
from universalassistant.core import CALLBACK_TYPE, UniversalAssistant
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN

TRIGGER_SCHEMA = probatio.All(
    toggle_entity.TRIGGER_SCHEMA,
    probatio.Schema(
        {probatio.Required(CONF_DOMAIN): DOMAIN}, extra=probatio.ALLOW_EXTRA
    ),
)


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for state changes based on configuration."""
    return await toggle_entity.async_attach_trigger(hass, config, action, trigger_info)


async def async_get_triggers(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers."""
    return await toggle_entity.async_get_triggers(hass, device_id, DOMAIN)


async def async_get_trigger_capabilities(
    hass: UniversalAssistant, config: ConfigType
) -> dict[str, probatio.Schema]:
    """List trigger capabilities."""
    return await toggle_entity.async_get_trigger_capabilities(hass, config)
