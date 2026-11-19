"""Tests for diagnostics data."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant


@pytest.mark.parametrize(
    "device_fixture",
    [
        "HWE-P1",
        "HWE-SKT-11",
        "HWE-SKT-21",
        "HWE-WTR",
        "SDM230",
        "SDM630",
        "HWE-KWH1",
        "HWE-KWH3",
        "HWE-BAT",
    ],
)
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )


@pytest.mark.parametrize("device_fixture", ["HWE-SKT"])
async def test_diagnostics_v2(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    init_integration_v2: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for devices using the v2 API."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration_v2)
        == snapshot
    )
