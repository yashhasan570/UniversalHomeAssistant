"""Tests for the Firefly III integration."""

from unittest.mock import AsyncMock

from pyfirefly.exceptions import (
    FireflyAuthenticationError,
    FireflyConnectionError,
    FireflyTimeoutError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import setup_integration


@pytest.mark.parametrize(
    ("exception", "expected_state"),
    [
        (FireflyAuthenticationError("bad creds"), ConfigEntryState.SETUP_ERROR),
        (FireflyConnectionError("cannot connect"), ConfigEntryState.SETUP_RETRY),
        (FireflyTimeoutError("timeout"), ConfigEntryState.SETUP_RETRY),
    ],
)
async def test_setup_exceptions(
    hass: UniversalAssistant,
    mock_firefly_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    exception: Exception,
    expected_state: ConfigEntryState,
) -> None:
    """Test the _async_setup."""
    mock_firefly_client.get_about.side_effect = exception
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is expected_state
