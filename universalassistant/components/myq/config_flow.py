"""Config flow for MyQ integration."""

from universalassistant.config_entries import ConfigFlow

from . import DOMAIN


class MyQConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MyQ."""

    VERSION = 1
