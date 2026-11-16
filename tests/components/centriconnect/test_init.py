"""Tests for the CentriConnect/MyPropane configuration initialization."""

from unittest.mock import AsyncMock

from aiocentriconnect.exceptions import CentriConnectConnectionError
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.centriconnect.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr

from . import setup_integration


async def test_device_info(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_centriconnect_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test device registry integration."""
    await setup_integration(hass, mock_config_entry)
    device_entry = device_registry.async_get_device_by_identifier(
        (DOMAIN, mock_config_entry.unique_id), mock_config_entry.entry_id
    )
    assert device_entry is not None
    assert device_entry == snapshot


async def test_config_entry_not_ready(
    hass: UniversalAssistant,
    mock_centriconnect_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test config entry not ready."""
    mock_centriconnect_client.async_get_tank_data.side_effect = (
        CentriConnectConnectionError
    )
    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
    mock_centriconnect_client.async_get_tank_data.side_effect = None
