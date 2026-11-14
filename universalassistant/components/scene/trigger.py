"""Provides triggers for scenes."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.automation import DomainSpec
from universalassistant.helpers.trigger import StatelessEntityTriggerBase, Trigger

from .const import DOMAIN


class SceneActivatedTrigger(StatelessEntityTriggerBase):
    """Trigger for scene entity activations."""

    _domain_specs = {DOMAIN: DomainSpec()}


TRIGGERS: dict[str, type[Trigger]] = {
    "activated": SceneActivatedTrigger,
}


async def async_get_triggers(hass: UniversalAssistant) -> dict[str, type[Trigger]]:
    """Return the triggers for scenes."""
    return TRIGGERS
