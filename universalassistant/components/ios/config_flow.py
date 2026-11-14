"""Config flow for iOS."""

from universalassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_discovery_flow(
    DOMAIN, "__HA_KEEP__ iOS", lambda hass: True
)
