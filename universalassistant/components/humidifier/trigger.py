"""Provides triggers for humidifiers."""

from typing import override

import probatio

from universalassistant.const import CONF_MODE, CONF_OPTIONS, STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.entity import get_supported_features
from universalassistant.helpers.trigger import (
    ENTITY_STATE_TRIGGER_SCHEMA_WITH_BEHAVIOR,
    EntityTargetStateTriggerBase,
    Trigger,
    TriggerConfig,
    make_entity_target_state_trigger,
)

from .const import (
    DOMAIN,
    HumidifierAction,
    HumidifierEntityFeature,
    HumidifierEntityStateAttribute,
)

MODE_CHANGED_TRIGGER_SCHEMA = ENTITY_STATE_TRIGGER_SCHEMA_WITH_BEHAVIOR.extend(
    {
        probatio.Required(CONF_OPTIONS): {
            probatio.Required(CONF_MODE): probatio.All(
                probatio.EnsureList(), probatio.NonEmpty(), [str]
            ),
        },
    }
)


def _supports_feature(hass: UniversalAssistant, entity_id: str, features: int) -> bool:
    """Test if an entity supports the specified features."""
    try:
        return bool(get_supported_features(hass, entity_id) & features)
    except UniversalAssistantError:
        return False


class ModeChangedTrigger(EntityTargetStateTriggerBase):
    """Trigger for humidifier mode changes."""

    _domain_specs = {
        DOMAIN: DomainSpec(value_source=HumidifierEntityStateAttribute.MODE)
    }
    _schema = MODE_CHANGED_TRIGGER_SCHEMA

    def __init__(self, hass: UniversalAssistant, config: TriggerConfig) -> None:
        """Initialize the mode trigger."""
        super().__init__(hass, config)
        self._to_states = set(self._options[CONF_MODE])

    @override
    def entity_filter(self, entities: set[str]) -> set[str]:
        """Filter entities of this domain."""
        entities = super().entity_filter(entities)
        return {
            entity_id
            for entity_id in entities
            if _supports_feature(self._hass, entity_id, HumidifierEntityFeature.MODES)
        }


TRIGGERS: dict[str, type[Trigger]] = {
    "mode_changed": ModeChangedTrigger,
    "started_drying": make_entity_target_state_trigger(
        {DOMAIN: DomainSpec(value_source=HumidifierEntityStateAttribute.ACTION)},
        HumidifierAction.DRYING,
    ),
    "started_humidifying": make_entity_target_state_trigger(
        {DOMAIN: DomainSpec(value_source=HumidifierEntityStateAttribute.ACTION)},
        HumidifierAction.HUMIDIFYING,
    ),
    "turned_off": make_entity_target_state_trigger(DOMAIN, STATE_OFF),
    "turned_on": make_entity_target_state_trigger(DOMAIN, STATE_ON),
}


async def async_get_triggers(hass: UniversalAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for humidifiers."""
    return TRIGGERS
