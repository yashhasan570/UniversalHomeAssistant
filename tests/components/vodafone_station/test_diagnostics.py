"""Tests for Vodafone Station diagnostics platform."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    mock_vodafone_station_router: AsyncMock,
    mock_config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await setup_integration(hass, mock_config_entry)

    assert await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    ) == snapshot(
        exclude=props(
            "entry_id",
            "created_at",
            "modified_at",
        )
    )
