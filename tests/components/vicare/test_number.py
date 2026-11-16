"""Test ViCare number entity."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import MODULE, setup_integration
from .conftest import Fixture, MockPyViCare


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    fixtures: list[Fixture] = [Fixture({"type:boiler"}, "vicare/Vitodens300W.json")]
    with (
        patch(
            "universalassistant.helpers.config_entry_oauth2_flow.OAuth2Session.async_ensure_token_valid",
        ),
        patch(f"{MODULE}.PyViCare", return_value=MockPyViCare(fixtures)),
        patch(f"{MODULE}.PLATFORMS", [Platform.NUMBER]),
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
