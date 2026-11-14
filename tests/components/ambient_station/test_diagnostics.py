"""Test Ambient PWS diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.ambient_station import AmbientStationConfigEntry
from universalassistant.core import UniversalAssistant


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    config_entry: AmbientStationConfigEntry,
    hass_client: ClientSessionGenerator,
    data_station,
    setup_config_entry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    ambient = config_entry.runtime_data
    ambient.stations = data_station
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(exclude=props("created_at", "modified_at"))
