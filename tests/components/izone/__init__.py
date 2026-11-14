"""IZone tests."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


async def setup_integration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Add and set up a config entry (discovery/controller must already be mocked)."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
