"""Tests for the diagnostics data provided by the YouTube integration."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.youtube.const import DOMAIN
from universalassistant.core import UniversalAssistant

from .conftest import ComponentSetup


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    setup_integration: ComponentSetup,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    await setup_integration()
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
