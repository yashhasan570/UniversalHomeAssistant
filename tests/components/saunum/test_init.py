"""Test Saunum Leil integration setup and teardown."""

from unittest.mock import patch

from pysaunum import SaunumConnectionError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.saunum.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr


async def test_setup_and_unload(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_saunum_client,
) -> None:
    """Test integration setup and unload."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_async_setup_entry_connection_failed(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_saunum_client,
) -> None:
    """Test integration setup fails when connection cannot be established."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.saunum.SaunumClient.create",
        side_effect=SaunumConnectionError("Connection failed"),
    ):
        assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
    assert mock_config_entry.error_reason_translation_key == "cannot_connect"
    assert mock_config_entry.error_reason_translation_placeholders == {
        "host": mock_config_entry.data["host"],
    }


@pytest.mark.usefixtures("init_integration")
async def test_device_entry(
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test device registry entry."""
    assert (
        device_entry := device_registry.async_get_device_by_identifier(
            (DOMAIN, mock_config_entry.entry_id), mock_config_entry.entry_id
        )
    )
    assert device_entry == snapshot
