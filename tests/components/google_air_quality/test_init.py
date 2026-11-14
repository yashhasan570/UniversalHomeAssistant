"""Tests for Google Air Quality."""

from unittest.mock import AsyncMock

from google_air_quality_api.exceptions import GoogleAirQualityApiError
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__


async def test_setup(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_api: AsyncMock,
) -> None:
    """Test successful setup and unload."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_with_custom_laqi(
    hass: __HAC_KEEP__,
    mock_config_entry_with_custom_laqi: MockConfigEntry,
    mock_api: AsyncMock,
) -> None:
    """Test successful setup with custom LAQI and unload."""
    mock_config_entry_with_custom_laqi.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry_with_custom_laqi.entry_id)
    assert mock_config_entry_with_custom_laqi.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry_with_custom_laqi.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry_with_custom_laqi.state is ConfigEntryState.NOT_LOADED


async def test_config_not_ready(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_api: AsyncMock,
) -> None:
    """Test for setup failure if an API call fails."""
    mock_config_entry.add_to_hass(hass)
    mock_api.async_get_current_conditions.side_effect = GoogleAirQualityApiError()

    await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
