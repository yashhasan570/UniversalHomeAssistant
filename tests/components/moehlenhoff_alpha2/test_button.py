"""Tests for the Moehlenhoff Alpha2 buttons."""

from unittest.mock import patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


async def test_buttons(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test buttons."""
    with patch(
        "universalassistant.components.moehlenhoff_alpha2.PLATFORMS",
        [Platform.BUTTON],
    ):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
