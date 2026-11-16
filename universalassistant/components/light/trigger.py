"""Provides triggers for lights."""

from typing import override

from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import UniversalAssistant, State
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import (
    EntityNumericalStateChangedTriggerBase,
    EntityNumericalStateCrossedThresholdTriggerBase,
    EntityNumericalStateTriggerBase,
    Trigger,
    make_entity_target_state_trigger,
)

from .const import DOMAIN, LightEntityStateAttribute

BRIGHTNESS_DOMAIN_SPECS: dict[str, DomainSpec] = {
    DOMAIN: DomainSpec(value_source=LightEntityStateAttribute.BRIGHTNESS),
}


class BrightnessTriggerMixin(EntityNumericalStateTriggerBase):
    """Mixin for brightness triggers."""

    _domain_specs = BRIGHTNESS_DOMAIN_SPECS
    _valid_unit = "%"

    @override
    def _get_tracked_value(self, state: State) -> float | None:
        """Get tracked brightness as a percentage."""
        value = super()._get_tracked_value(state)
        if value is None:
            return None
        # Convert uint8 value (0-255) to a percentage (0-100)
        return (value / 255.0) * 100.0


class BrightnessChangedTrigger(
    EntityNumericalStateChangedTriggerBase, BrightnessTriggerMixin
):
    """Trigger for light brightness changes."""


class BrightnessCrossedThresholdTrigger(
    EntityNumericalStateCrossedThresholdTriggerBase, BrightnessTriggerMixin
):
    """Trigger for light brightness crossing a threshold."""


TRIGGERS: dict[str, type[Trigger]] = {
    "brightness_changed": BrightnessChangedTrigger,
    "brightness_crossed_threshold": BrightnessCrossedThresholdTrigger,
    "turned_off": make_entity_target_state_trigger(DOMAIN, STATE_OFF),
    "turned_on": make_entity_target_state_trigger(DOMAIN, STATE_ON),
}


async def async_get_triggers(hass: UniversalAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for lights."""
    return TRIGGERS
