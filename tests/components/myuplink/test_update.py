"""Tests for myuplink update module."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_update_states(
    hass: UniversalAssistant,
    mock_myuplink_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test update state."""
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("update.gotham_city_firmware")
    assert state is not None
    assert state.state == "off"
