"""Component to configure Universal Home Assistant via an API."""

from universalassistant.components import frontend
from universalassistant.const import EVENT_COMPONENT_LOADED
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.typing import ConfigType
from universalassistant.setup import EventComponentLoaded

from . import (
    area_registry,
    auth,
    auth_provider_universalassistant,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    scene,
    script,
)
from .const import DOMAIN

SECTIONS = (
    area_registry,
    auth,
    auth_provider_universalassistant,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    script,
    scene,
)


CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

__all__ = [
    "DOMAIN",
]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the config component."""
    frontend.async_register_built_in_panel(
        hass, "config", "config", "mdi:cog", require_admin=True
    )

    for panel in SECTIONS:
        if panel.async_setup(hass):
            name = panel.__name__.split(".")[-1]
            key = f"{DOMAIN}.{name}"
            hass.bus.async_fire(
                EVENT_COMPONENT_LOADED, EventComponentLoaded(component=key)
            )

    return True
