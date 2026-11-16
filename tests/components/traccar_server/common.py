"""Common test tools for Traccar Server."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_integration(hass: UniversalAssistant, config_entry: MockConfigEntry) -> None:
    """Set up the integration."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
