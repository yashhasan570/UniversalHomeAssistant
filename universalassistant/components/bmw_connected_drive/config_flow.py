"""The BMW Connected Drive integration config flow."""

from universalassistant.config_entries import ConfigFlow

from . import DOMAIN


class BMWConnectedDriveConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BMW Connected Drive."""
