"""Tests for the devolo Home Network diagnostics."""

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import configure_integration


@pytest.mark.usefixtures("mock_device")
async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    entry = configure_integration(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    result = await get_diagnostics_for_config_entry(hass, hass_client, entry)
    assert result == snapshot(exclude=props("created_at", "modified_at"))
