"""Tests for SleepIQ diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__

from .conftest import setup_platform


@pytest.mark.usefixtures("mock_asyncsleepiq")
async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics leave out account identifiers."""
    entry = await setup_platform(hass, "sensor")

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
