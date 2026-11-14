"""Config flow for GPSLogger."""

from universalassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "GPSLogger Webhook",
    {"docs_url": "https://www.universalassistant.io/integrations/gpslogger/"},
)
