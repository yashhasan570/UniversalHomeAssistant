"""Tests for the Ambient Weather Network diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from .conftest import setup_platform


@pytest.mark.parametrize(
    "config_entry",
    ["AA:AA:AA:AA:AA:AA", "DD:DD:DD:DD:DD:DD"],
    indirect=True,
)
@pytest.mark.usefixtures("aioambient")
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    await setup_platform(True, hass, config_entry)
    assert config_entry.state is ConfigEntryState.LOADED

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )
