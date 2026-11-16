"""Tests for the Glances diagnostics."""

from unittest.mock import MagicMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.glances.const import DOMAIN
from universalassistant.core import UniversalAssistant

from . import MOCK_USER_INPUT


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_api: MagicMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    mock_api.return_value.version = 4
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_USER_INPUT, entry_id="test")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
