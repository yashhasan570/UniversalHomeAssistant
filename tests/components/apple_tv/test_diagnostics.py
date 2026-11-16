"""Tests for the Apple TV diagnostics."""

from unittest.mock import AsyncMock

from pyatv.const import FeatureName, FeatureState
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
    mock_atv: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    mock_atv.features.set_state(FeatureName.Artwork, FeatureState.Unavailable)
    mock_atv.features.set_state(FeatureName.Stop, FeatureState.Unsupported)
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )
