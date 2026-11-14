"""Tests for the devolo_home_control integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.devolo_home_control.const import DOMAIN
from universalassistant.core import UniversalAssistant


def configure_integration(hass: UniversalAssistant) -> MockConfigEntry:
    """Configure the integration."""
    config = {
        "username": "test-username",
        "password": "test-password",
    }
    entry = MockConfigEntry(
        domain=DOMAIN, data=config, entry_id="123456", unique_id="123456"
    )
    entry.add_to_hass(hass)

    return entry
