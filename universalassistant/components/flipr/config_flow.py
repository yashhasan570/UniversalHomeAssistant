"""Config flow for Flipr integration."""

from universalassistant.config_entries import ConfigFlow

from . import DOMAIN


class FliprConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Flipr."""

    VERSION = 2
