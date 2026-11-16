"""Tests for Starlink diagnostics."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.starlink.const import DOMAIN
from universalassistant.const import CONF_IP_ADDRESS
from universalassistant.core import UniversalAssistant

from .patchers import (
    HISTORY_STATS_SUCCESS_PATCHER,
    LOCATION_DATA_SUCCESS_PATCHER,
    SLEEP_DATA_SUCCESS_PATCHER,
    STATUS_DATA_SUCCESS_PATCHER,
)


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_IP_ADDRESS: "1.2.3.4:0000"},
    )

    with (
        STATUS_DATA_SUCCESS_PATCHER,
        LOCATION_DATA_SUCCESS_PATCHER,
        SLEEP_DATA_SUCCESS_PATCHER,
        HISTORY_STATS_SUCCESS_PATCHER,
    ):
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)

        assert diag == snapshot
