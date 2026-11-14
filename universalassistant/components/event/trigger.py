"""Provides triggers for events."""

from typing import override

import probatio

from universalassistant.const import CONF_OPTIONS
from universalassistant.core import __HAC_KEEP__, State
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import (
    ENTITY_STATE_TRIGGER_SCHEMA,
    NotTriggeredReasonReporter,
    StatelessEntityTriggerBase,
    Trigger,
    TriggerConfig,
)

from .const import DOMAIN, EventEntityStateAttribute

CONF_EVENT_TYPE = "event_type"

EVENT_RECEIVED_TRIGGER_SCHEMA = ENTITY_STATE_TRIGGER_SCHEMA.extend(
    {
        probatio.Required(CONF_OPTIONS): {
            probatio.Required(CONF_EVENT_TYPE): probatio.All(
                probatio.EnsureList(), probatio.NonEmpty(), [cv.string]
            ),
        },
    }
)


class EventReceivedTrigger(StatelessEntityTriggerBase):
    """Trigger for event entity when it receives a matching event."""

    _domain_specs = {DOMAIN: DomainSpec()}
    _schema = EVENT_RECEIVED_TRIGGER_SCHEMA

    def __init__(self, hass: __HAC_KEEP__, config: TriggerConfig) -> None:
        """Initialize the event received trigger."""
        super().__init__(hass, config)
        self._event_types = set(self._options[CONF_EVENT_TYPE])

    @override
    def is_valid_state(
        self,
        state: State,
        report_not_triggered: NotTriggeredReasonReporter,
    ) -> bool:
        """Check if the event type matches one of the configured types."""
        return (
            state.attributes.get(EventEntityStateAttribute.EVENT_TYPE)
            in self._event_types
        )


TRIGGERS: dict[str, type[Trigger]] = {
    "received": EventReceivedTrigger,
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for events."""
    return TRIGGERS
