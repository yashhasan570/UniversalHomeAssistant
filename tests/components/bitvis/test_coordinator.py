"""Tests for the Bitvis Power Hub coordinator."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from .conftest import FakeListener

pytestmark = pytest.mark.usefixtures("patch_shared_listener")


async def test_setup_oserror_results_in_setup_retry(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_shared_listener: FakeListener,
) -> None:
    """Test that OSError from SharedListener.start results in SETUP_RETRY."""
    mock_shared_listener.start = AsyncMock(side_effect=OSError("port in use"))
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_runtime_error_results_in_setup_error(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_shared_listener: FakeListener,
) -> None:
    """Test that RuntimeError from SharedListener.register results in SETUP_ERROR."""
    mock_shared_listener.register.side_effect = RuntimeError("duplicate filter")
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    mock_shared_listener.unregister.assert_not_called()
