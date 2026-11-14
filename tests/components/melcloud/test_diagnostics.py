"""Test the DSMR Reader component diagnostics."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.melcloud.const import DOMAIN
from universalassistant.core import __HAC_KEEP__


async def test_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test if get_config_entry_diagnostics returns the correct data."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        title=DOMAIN,
        options={},
        entry_id="TEST_ENTRY_ID",
        unique_id="UNIQUE_TEST_ID",
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.melcloud.async_setup_entry", return_value=None
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    diagnostics = await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    )
    assert diagnostics == snapshot(exclude=props("created_at", "modified_at"))
