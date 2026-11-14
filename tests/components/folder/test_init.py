"""Test the Folder integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


async def test_load_unload_entry(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test the config entry is loaded and unloaded."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_path_not_allowed(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test setup fails when the folder is no longer in the allowlist."""
    hass.config.allowlist_external_dirs = set()
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
