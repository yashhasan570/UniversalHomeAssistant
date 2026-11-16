"""Provide the device conditions for Select."""

import probatio

from universalassistant.components.device_automation import (
    async_get_entity_registry_entry_or_raise,
)
from universalassistant.const import (
    CONF_CONDITION,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_FOR,
    CONF_TYPE,
)
from universalassistant.core import UniversalAssistant, callback
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import (
    condition,
    config_validation as cv,
    entity_registry as er,
)
from universalassistant.helpers.config_validation import DEVICE_CONDITION_BASE_SCHEMA
from universalassistant.helpers.entity import get_capability
from universalassistant.helpers.typing import ConfigType, TemplateVarsType

from .const import CONF_OPTION, DOMAIN, SelectEntityCapabilityAttribute

# nypy: disallow-any-generics

CONDITION_TYPES = {"selected_option"}

CONDITION_SCHEMA = DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
        probatio.Required(CONF_TYPE): probatio.In(CONDITION_TYPES),
        probatio.Required(CONF_OPTION): str,
        probatio.Optional(CONF_FOR): cv.positive_time_period_dict,
    }
)


async def async_get_conditions(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device conditions for Select devices."""
    registry = er.async_get(hass)
    return [
        {
            CONF_CONDITION: "device",
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_ENTITY_ID: entry.id,
            CONF_TYPE: "selected_option",
        }
        for entry in er.async_entries_for_device(registry, device_id)
        if entry.domain == DOMAIN
    ]


@callback
def async_condition_from_config(
    hass: UniversalAssistant, config: ConfigType
) -> condition.ConditionCheckerType:
    """Create a function to test a device condition."""

    registry = er.async_get(hass)
    entity_id = er.async_resolve_entity_id(registry, config[CONF_ENTITY_ID])

    @callback
    def test_is_state(hass: UniversalAssistant, variables: TemplateVarsType) -> bool:
        """Test if an entity is a certain state."""
        return condition.state(
            hass, entity_id, config[CONF_OPTION], config.get(CONF_FOR)
        )

    return test_is_state


async def async_get_condition_capabilities(
    hass: UniversalAssistant, config: ConfigType
) -> dict[str, probatio.Schema]:
    """List condition capabilities."""

    try:
        entry = async_get_entity_registry_entry_or_raise(hass, config[CONF_ENTITY_ID])
        options = (
            get_capability(
                hass, entry.entity_id, SelectEntityCapabilityAttribute.OPTIONS
            )
            or []
        )
    except UniversalAssistantError:
        options = []

    return {
        "extra_fields": probatio.Schema(
            {
                probatio.Required(CONF_OPTION): probatio.In(options),
                probatio.Optional(CONF_FOR): cv.positive_time_period_dict,
            }
        )
    }
