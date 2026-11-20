"""Test the PrusaLink diagnostics."""

from typing import Any

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant


@pytest.mark.usefixtures("mock_api")
async def test_diagnostics_no_job(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics while no job is running."""
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )


@pytest.mark.usefixtures("mock_api")
async def test_diagnostics_active_job(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    mock_get_status_printing: dict[str, Any],
    mock_job_api_printing: dict[str, Any],
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics while a job is running."""
    # The status message is free text, so the snapshot shows it is left out
    mock_get_status_printing["printer"]["status_printer"] = {
        "ok": True,
        "message": "Ready",
    }
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
