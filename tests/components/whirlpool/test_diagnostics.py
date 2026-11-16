"""Test Blink diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import UniversalAssistant

from . import init_integration

YAML_CONFIG = {"username": "test-user", "password": "test-password"}


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""

    mock_entry = await init_integration(hass)

    result = await get_diagnostics_for_config_entry(hass, hass_client, mock_entry)

    assert result == snapshot(exclude=props("entry_id", "created_at", "modified_at"))
