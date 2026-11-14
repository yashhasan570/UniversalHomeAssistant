"""Test Jellyfin diagnostics."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant


async def test_diagnostics(
    hass: UniversalAssistant,
    init_integration: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    data = await get_diagnostics_for_config_entry(hass, hass_client, init_integration)

    assert data["entry"]["data"]["client_device_id"] == init_integration.entry_id
    data["entry"]["data"]["client_device_id"] = "entry-id"

    assert data == snapshot
