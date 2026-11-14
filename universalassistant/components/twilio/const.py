"""Const for Twilio."""

from typing import TYPE_CHECKING

from universalassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from twilio.rest import Client

DOMAIN = "twilio"

DATA_TWILIO: HassKey[Client] = HassKey(DOMAIN)
