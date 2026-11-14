"""Constants for the Foursquare integration."""

from universalassistant.util.hass_dict import HassKey

CONF_PUSH_SECRET = "push_secret"

DOMAIN = "foursquare"

DATA_ACCESS_TOKEN: HassKey[str] = HassKey(DOMAIN)

EVENT_CHECKIN = "foursquare.checkin"
EVENT_PUSH = "foursquare.push"
