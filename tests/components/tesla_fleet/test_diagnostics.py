"""Test the Tesla Fleet Diagnostics."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import setup_platform


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    normal_config_entry: MockConfigEntry,
) -> None:
    """Test diagnostics."""

    await setup_platform(hass, normal_config_entry)

    diag = await get_diagnostics_for_config_entry(
        hass, hass_client, normal_config_entry
    )
    assert diag == snapshot
