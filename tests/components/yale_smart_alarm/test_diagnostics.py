"""Test Yale Smart Living diagnostics."""

from unittest.mock import Mock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    load_config_entry: tuple[MockConfigEntry, Mock],
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    entry = load_config_entry[0]

    diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert diag == snapshot
