"""Config flow for the Sleep as Android integration."""

from universalassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Sleep as Android",
    {"docs_url": "https://www.universalassistant.io/integrations/sleep_as_android"},
    allow_multiple=True,
)
