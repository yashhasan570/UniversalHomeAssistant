"""Test the Fast.com component diagnostics."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.fastdotcom.const import DEFAULT_NAME, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import __HAC_KEEP__

from . import MOCK_DATA


async def test_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test if get_config_entry_diagnostics returns the correct data."""
    config_entry = MockConfigEntry(
        version=1,
        domain=DOMAIN,
        title=DEFAULT_NAME,
        source=SOURCE_USER,
        options={},
        entry_id="TEST_ENTRY_ID",
        unique_id="UNIQUE_TEST_ID",
        minor_version=1,
    )
    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.fastdotcom.coordinator.fast_com",
        return_value=MOCK_DATA,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )
