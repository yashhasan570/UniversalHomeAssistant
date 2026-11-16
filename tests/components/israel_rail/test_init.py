"""Test init of israel_rail integration."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import init_integration


async def test_invalid_config(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_israelrail: AsyncMock,
) -> None:
    """Ensure nothing is created when config is wrong."""
    mock_israelrail.query.side_effect = Exception("error")
    await init_integration(hass, mock_config_entry)
    assert not hass.states.async_entity_ids("sensor")
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
