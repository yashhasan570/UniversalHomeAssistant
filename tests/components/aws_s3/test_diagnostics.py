"""Tests for AWS S3 diagnostics."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.backup import DOMAIN as BACKUP_DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    mock_config_entry.add_to_hass(hass)
    assert await async_setup_component(hass, BACKUP_DOMAIN, {BACKUP_DOMAIN: {}})
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
