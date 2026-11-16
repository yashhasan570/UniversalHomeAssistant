"""Support for Twilio."""

from aiohttp import web
import probatio
from twilio.rest import Client

from universalassistant.components import webhook
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_WEBHOOK_ID
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_entry_flow, config_validation as cv
from universalassistant.helpers.typing import ConfigType

from .const import DATA_TWILIO, DOMAIN

CONF_ACCOUNT_SID = "account_sid"
CONF_AUTH_TOKEN = "auth_token"

RECEIVED_DATA = f"{DOMAIN}_data_received"

CONFIG_SCHEMA = probatio.Schema(
    {
        probatio.Optional(DOMAIN): probatio.Schema(
            {
                probatio.Required(CONF_ACCOUNT_SID): cv.string,
                probatio.Required(probatio.Secret(CONF_AUTH_TOKEN)): cv.string,
            }
        )
    },
    extra=probatio.ALLOW_EXTRA,
)

__all__ = [
    "DOMAIN",
    "get_client",
]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Twilio component."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    hass.data[DATA_TWILIO] = await hass.async_add_executor_job(
        Client, conf.get(CONF_ACCOUNT_SID), conf.get(CONF_AUTH_TOKEN)
    )
    return True


def get_client(hass: UniversalAssistant) -> Client:
    """Return the Twilio client."""
    return hass.data[DATA_TWILIO]


async def handle_webhook(
    hass: UniversalAssistant, webhook_id: str, request: web.Request
) -> web.Response:
    """Handle incoming webhook from Twilio for inbound messages and calls."""
    data = dict(await request.post())
    data["webhook_id"] = webhook_id
    hass.bus.async_fire(RECEIVED_DATA, dict(data))

    return web.Response(text="")


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Configure based on config entry."""
    webhook.async_register(
        hass, DOMAIN, "Twilio", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])


async_remove_entry = config_entry_flow.webhook_async_remove_entry
