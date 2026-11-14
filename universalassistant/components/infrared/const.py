"""Constants for the Infrared integration."""

from typing import Final

from universalassistant.helpers.entity_component import EntityComponent
from universalassistant.util.hass_dict import HassKey

from .entity import InfraredEmitterEntity, InfraredReceiverEntity

DOMAIN: Final = "infrared"
DATA_COMPONENT: HassKey[
    EntityComponent[InfraredEmitterEntity | InfraredReceiverEntity]
] = HassKey(DOMAIN)
