"""Provides device conditions for remotes."""

import probatio

from universalassistant.components.device_automation import toggle_entity
from universalassistant.const import CONF_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.condition import ConditionCheckerType
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN

# mypy: disallow-any-generics

CONDITION_SCHEMA = toggle_entity.CONDITION_SCHEMA.extend(
    {probatio.Required(CONF_DOMAIN): DOMAIN}
)


@callback
def async_condition_from_config(
    hass: __HAC_KEEP__, config: ConfigType
) -> ConditionCheckerType:
    """Evaluate state based on configuration."""
    return toggle_entity.async_condition_from_config(hass, config)


async def async_get_conditions(
    hass: __HAC_KEEP__, device_id: str
) -> list[dict[str, str]]:
    """List device conditions."""
    return await toggle_entity.async_get_conditions(hass, device_id, DOMAIN)


async def async_get_condition_capabilities(
    hass: __HAC_KEEP__, config: ConfigType
) -> dict[str, probatio.Schema]:
    """List condition capabilities."""
    return await toggle_entity.async_get_condition_capabilities(hass, config)
