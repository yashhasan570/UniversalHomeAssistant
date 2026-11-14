"""Tests for the Version integration setup."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.version.const import CONF_BOARD, DEFAULT_CONFIGURATION
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from .common import MOCK_VERSION_CONFIG_ENTRY_DATA


async def test_setup_invalid_board(hass: __HAC_KEEP__) -> None:
    """Test setup fails when the configured board is no longer valid."""
    entry = MockConfigEntry(
        **{
            **MOCK_VERSION_CONFIG_ENTRY_DATA,
            "data": {**DEFAULT_CONFIGURATION, CONF_BOARD: "Not a board"},
        }
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == (
        'Board "Not a board" is (no longer) valid. Please remove the integration'
        ' "Local installation"'
    )
