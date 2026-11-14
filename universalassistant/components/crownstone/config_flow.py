"""Flow handler for Crownstone."""

from universalassistant.config_entries import ConfigFlow

from . import DOMAIN


class CrownstoneConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crownstone."""

    VERSION = 1
