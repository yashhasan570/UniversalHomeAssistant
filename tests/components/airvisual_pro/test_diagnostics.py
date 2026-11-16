"""Test AirVisual Pro diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import UniversalAssistant


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    config_entry,
    hass_client: ClientSessionGenerator,
    setup_airvisual_pro,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(exclude=props("created_at", "modified_at"))
