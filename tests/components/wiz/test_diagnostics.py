"""Test WiZ diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import async_setup_integration


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    _, entry = await async_setup_integration(hass)

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
