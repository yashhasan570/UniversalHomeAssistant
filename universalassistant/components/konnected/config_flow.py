"""Config flow for Konnected.io integration."""

from universalassistant.config_entries import ConfigFlow

from .const import DOMAIN


class KonnectedFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Konnected.io."""

    VERSION = 1
