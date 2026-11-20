"""Tests for the qBittorrent diagnostics."""

from typing import Any

import pytest
from pytest_universalassistant.common import MockConfigEntry, load_json_object_fixture
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.qbittorrent.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

SYNC_MAINDATA = load_json_object_fixture("sync_maindata.json", DOMAIN)


@pytest.mark.parametrize(
    "sync_maindata",
    [
        pytest.param(SYNC_MAINDATA, id="with_torrents"),
        pytest.param(
            {key: value for key, value in SYNC_MAINDATA.items() if key != "torrents"},
            id="without_torrents",
        ),
    ],
)
@pytest.mark.usefixtures("mock_qbittorrent")
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    sync_maindata: dict[str, Any],
) -> None:
    """Test diagnostics."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
