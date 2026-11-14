"""The Fitbit integration config flow."""

from universalassistant.config_entries import ConfigFlow

from . import DOMAIN


class FitbitConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fitbit."""
