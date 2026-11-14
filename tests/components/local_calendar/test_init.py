"""Tests for init platform of local calendar."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from .conftest import TEST_ENTITY


async def test_load_unload(
    hass: __HAC_KEEP__, setup_integration: None, config_entry: MockConfigEntry
) -> None:
    """Test loading and unloading a config entry."""

    assert config_entry.state is ConfigEntryState.LOADED

    state = hass.states.get(TEST_ENTITY)
    assert state
    assert state.state == "off"

    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.NOT_LOADED
    state = hass.states.get(TEST_ENTITY)
    assert state
    assert state.state == "unavailable"


async def test_remove_config_entry(
    hass: __HAC_KEEP__, setup_integration: None, config_entry: MockConfigEntry
) -> None:
    """Test removing a config entry."""

    with patch("universalassistant.components.local_calendar.Path.unlink") as unlink_mock:
        assert await hass.config_entries.async_remove(config_entry.entry_id)
        await hass.async_block_till_done()
        unlink_mock.assert_called_once()


@pytest.mark.parametrize(
    ("store_read_side_effect"),
    [
        (OSError("read error")),
    ],
)
async def test_load_failure(
    hass: __HAC_KEEP__, setup_integration: None, config_entry: MockConfigEntry
) -> None:
    """Test failures loading the store."""

    assert config_entry.state is ConfigEntryState.SETUP_RETRY

    state = hass.states.get(TEST_ENTITY)
    assert not state
