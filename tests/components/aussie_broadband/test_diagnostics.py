"""Test the Aussie Broadband Diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from .common import setup_platform


async def test_select_async_setup_entry(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics platform."""

    entry = await setup_platform(hass, [])
    diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)
    assert diag == snapshot
