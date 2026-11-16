"""Test the Firefly III component diagnostics."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_get_config_entry_diagnostics(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_firefly_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test if get_config_entry_diagnostics returns the correct data."""
    await setup_integration(hass, mock_config_entry)

    diagnostics_entry = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )
    assert diagnostics_entry == snapshot(
        exclude=props(
            "created_at",
            "modified_at",
        )
    )
