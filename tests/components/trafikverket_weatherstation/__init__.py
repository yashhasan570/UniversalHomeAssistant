"""Tests for the Trafikverket weatherstation integration."""

from universalassistant.components.trafikverket_weatherstation.const import CONF_STATION
from universalassistant.const import CONF_API_KEY

ENTRY_CONFIG = {
    CONF_API_KEY: "1234567890",
    CONF_STATION: "Arlanda",
}
