"""Constants for the Meater Temperature Probe integration."""

from universalassistant.util.hass_dict import HassKey

DOMAIN = "meater"

MEATER_DATA: HassKey[set[str]] = HassKey(DOMAIN)
