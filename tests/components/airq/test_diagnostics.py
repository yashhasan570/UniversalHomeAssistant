"""Test air-Q diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.airq.const import DOMAIN
from universalassistant.core import UniversalAssistant

from .common import TEST_DEVICE_INFO, TEST_USER_DATA

FIXED_MOCK_ENTRY_ID = "01JGFJJZ008DNE3BKJ7ZE14YFE"


@pytest.mark.freeze_time("2025-01-01T00:00:00+00:00")
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_airq,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=TEST_USER_DATA,
        unique_id=TEST_DEVICE_INFO["id"],
        entry_id=FIXED_MOCK_ENTRY_ID,
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert result == snapshot
