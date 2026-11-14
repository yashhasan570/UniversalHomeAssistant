"""Tests the diagnostics for Universal Universal Home Assistant Backup integration."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.backup.const import DOMAIN
from universalassistant.core import UniversalAssistant

from .common import setup_backup_integration


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    await setup_backup_integration(hass, with_hassio=False)
    await hass.async_block_till_done(wait_background_tasks=True)

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    diag_data = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert diag_data == snapshot
