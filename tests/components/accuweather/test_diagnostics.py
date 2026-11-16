"""Test AccuWeather diagnostics."""

from unittest.mock import AsyncMock

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import init_integration


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_accuweather_client: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    entry = await init_integration(hass)

    result = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert result == snapshot
