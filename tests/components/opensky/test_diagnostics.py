"""Tests for the OpenSky diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import setup_integration


@pytest.mark.usefixtures("opensky_client")
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    config_entry_authenticated: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    await setup_integration(hass, config_entry_authenticated)

    assert (
        await get_diagnostics_for_config_entry(
            hass, hass_client, config_entry_authenticated
        )
        == snapshot
    )
