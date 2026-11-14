"""Provides device automations for Fan."""

import probatio

from universalassistant.components.device_automation import (
    async_validate_entity_schema,
    toggle_entity,
)
from universalassistant.const import CONF_DOMAIN
from universalassistant.core import Context, UniversalAssistant
from universalassistant.helpers.typing import ConfigType, TemplateVarsType

from .const import DOMAIN

_ACTION_SCHEMA = toggle_entity.ACTION_SCHEMA.extend(
    {probatio.Required(CONF_DOMAIN): DOMAIN}
)


async def async_validate_action_config(
    hass: UniversalAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return async_validate_entity_schema(hass, config, _ACTION_SCHEMA)


async def async_get_actions(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device actions for Fan devices."""
    return await toggle_entity.async_get_actions(hass, device_id, DOMAIN)


async def async_call_action_from_config(
    hass: UniversalAssistant,
    config: ConfigType,
    variables: TemplateVarsType,
    context: Context | None,
) -> None:
    """Execute a device action."""
    await toggle_entity.async_call_action_from_config(
        hass, config, variables, context, DOMAIN
    )
