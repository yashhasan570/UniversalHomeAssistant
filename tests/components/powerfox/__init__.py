"""Tests for the Powerfox integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant

MOCK_DIRECT_HOST = "1.1.1.1"


async def setup_integration(hass: UniversalAssistant, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the integration."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
