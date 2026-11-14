"""Test RainMachine select entities."""

from typing import Any
from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.rainmachine.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.setup import async_setup_component


async def test_select_entities(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    config: dict[str, Any],
    config_entry: MockConfigEntry,
    client: AsyncMock,
) -> None:
    """Test select entities."""
    with (
        patch("universalassistant.components.rainmachine.Client", return_value=client),
        patch("universalassistant.components.rainmachine.PLATFORMS", [Platform.SELECT]),
    ):
        assert await async_setup_component(hass, DOMAIN, config)
        await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
