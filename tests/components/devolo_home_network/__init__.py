"""Tests for the devolo Home Network integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.devolo_home_network.const import DOMAIN
from universalassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__

from .const import DISCOVERY_INFO, IP


def configure_integration(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Configure the integration."""
    config = {
        CONF_IP_ADDRESS: IP,
        CONF_PASSWORD: "test",
    }
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=config,
        entry_id="123456",
        unique_id=DISCOVERY_INFO.properties["SN"],
    )
    entry.add_to_hass(hass)

    return entry
