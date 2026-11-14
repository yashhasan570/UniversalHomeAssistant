"""Config flow for JuiceNet integration."""

from universalassistant.config_entries import ConfigFlow

from .const import DOMAIN


class JuiceNetConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JuiceNet."""

    VERSION = 1
