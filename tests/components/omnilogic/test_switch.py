"""Tests for the omnilogic switches."""

from unittest.mock import patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


async def test_switches(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test switches."""
    with patch(
        "universalassistant.components.omnilogic.PLATFORMS",
        [Platform.SWITCH],
    ):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
