"""Offer device oriented automation."""

from typing import Any, Protocol

import probatio

from universalassistant.const import CONF_DOMAIN
from universalassistant.core import CALLBACK_TYPE, UniversalAssistant
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from . import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    DeviceAutomationType,
    async_get_device_automation_platform,
)
from .helpers import async_validate_device_automation_config

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend({}, extra=probatio.ALLOW_EXTRA)


class DeviceAutomationTriggerProtocol(Protocol):
    """Define the format of device_trigger modules.

    Each module must define either TRIGGER_SCHEMA or async_validate_trigger_config.
    """

    TRIGGER_SCHEMA: probatio.Schema

    async def async_validate_trigger_config(
        self, hass: UniversalAssistant, config: ConfigType
    ) -> ConfigType:
        """Validate config."""

    async def async_attach_trigger(
        self,
        hass: UniversalAssistant,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CALLBACK_TYPE:
        """Attach a trigger."""

    async def async_get_trigger_capabilities(
        self, hass: UniversalAssistant, config: ConfigType
    ) -> dict[str, probatio.Schema]:
        """List trigger capabilities."""

    async def async_get_triggers(
        self, hass: UniversalAssistant, device_id: str
    ) -> list[dict[str, Any]]:
        """List triggers."""


async def async_validate_trigger_config(
    hass: UniversalAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return await async_validate_device_automation_config(
        hass, config, TRIGGER_SCHEMA, DeviceAutomationType.TRIGGER
    )


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for trigger."""
    platform = await async_get_device_automation_platform(
        hass, config[CONF_DOMAIN], DeviceAutomationType.TRIGGER
    )
    return await platform.async_attach_trigger(hass, config, action, trigger_info)
