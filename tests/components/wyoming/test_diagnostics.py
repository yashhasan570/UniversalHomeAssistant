"""Tests for the Wyoming diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant


@pytest.mark.usefixtures("init_wyoming_stt")
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    stt_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for a service config entry."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, stt_config_entry)
        == snapshot
    )


@pytest.mark.usefixtures("init_satellite")
async def test_diagnostics_satellite(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    satellite_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for a satellite config entry."""
    assert (
        await get_diagnostics_for_config_entry(
            hass, hass_client, satellite_config_entry
        )
        == snapshot
    )
