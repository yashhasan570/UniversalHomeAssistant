"""Provides triggers for doorbells."""

from typing import override

from universalassistant.components.event import (
    DOMAIN as EVENT_DOMAIN,
    DoorbellEventType,
    EventDeviceClass,
    EventEntityStateAttribute,
)
from universalassistant.core import __HAC_KEEP__, State
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import (
    NotTriggeredReasonReporter,
    StatelessEntityTriggerBase,
    Trigger,
)


class DoorbellRangTrigger(StatelessEntityTriggerBase):
    """Trigger for doorbell event entity when a ring event is received."""

    _domain_specs = {EVENT_DOMAIN: DomainSpec(device_class=EventDeviceClass.DOORBELL)}

    @override
    def is_valid_state(
        self,
        state: State,
        report_not_triggered: NotTriggeredReasonReporter,
    ) -> bool:
        """Check if the event type is ring."""
        return (
            state.attributes.get(EventEntityStateAttribute.EVENT_TYPE)
            == DoorbellEventType.RING
        )


TRIGGERS: dict[str, type[Trigger]] = {
    "rang": DoorbellRangTrigger,
}


async def async_get_triggers(hass: __HAC_KEEP__) -> dict[str, type[Trigger]]:
    """Return the triggers for doorbells."""
    return TRIGGERS
