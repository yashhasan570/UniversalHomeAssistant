"""The tests for the Backup event entity."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import snapshot_platform
from pytest_universalassistant.typing import WebSocketGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.backup.const import DOMAIN
from universalassistant.components.backup.event import ATTR_BACKUP_STAGE, ATTR_FAILED_REASON
from universalassistant.components.event import EventEntityStateAttribute
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .common import setup_backup_integration


async def test_event_entity(
    hass: __HAC_KEEP__,
    hass_ws_client: WebSocketGenerator,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test automatic backup event entity."""
    with patch("universalassistant.components.backup.PLATFORMS", [Platform.EVENT]):
        await setup_backup_integration(hass, with_hassio=False)
        await hass.async_block_till_done(wait_background_tasks=True)

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_event_entity_backup_completed(
    hass: __HAC_KEEP__,
    hass_ws_client: WebSocketGenerator,
) -> None:
    """Test completed automatic backup event."""
    with patch("universalassistant.components.backup.PLATFORMS", [Platform.EVENT]):
        await setup_backup_integration(hass, with_hassio=False)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("event.backup_automatic_backup")
    assert state.attributes[EventEntityStateAttribute.EVENT_TYPE] is None

    client = await hass_ws_client(hass)
    await hass.async_block_till_done()
    await client.send_json_auto_id(
        {"type": "backup/generate", "agent_ids": ["backup.local"]}
    )
    assert await client.receive_json()

    state = hass.states.get("event.backup_automatic_backup")
    assert state.attributes[EventEntityStateAttribute.EVENT_TYPE] == "in_progress"
    assert state.attributes[ATTR_BACKUP_STAGE] is not None
    assert state.attributes[ATTR_FAILED_REASON] is None

    await hass.async_block_till_done(wait_background_tasks=True)
    state = hass.states.get("event.backup_automatic_backup")
    assert state.attributes[EventEntityStateAttribute.EVENT_TYPE] == "completed"
    assert state.attributes[ATTR_BACKUP_STAGE] is None
    assert state.attributes[ATTR_FAILED_REASON] is None


async def test_event_entity_backup_failed(
    hass: __HAC_KEEP__,
    hass_ws_client: WebSocketGenerator,
    create_backup: AsyncMock,
) -> None:
    """Test failed automatic backup event."""
    with patch("universalassistant.components.backup.PLATFORMS", [Platform.EVENT]):
        await setup_backup_integration(hass, with_hassio=False)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("event.backup_automatic_backup")
    assert state.attributes[EventEntityStateAttribute.EVENT_TYPE] is None

    create_backup.side_effect = Exception("Boom!")

    client = await hass_ws_client(hass)
    await hass.async_block_till_done()
    await client.send_json_auto_id(
        {"type": "backup/generate", "agent_ids": ["backup.local"]}
    )
    assert await client.receive_json()

    state = hass.states.get("event.backup_automatic_backup")
    assert state.attributes[EventEntityStateAttribute.EVENT_TYPE] == "failed"
    assert state.attributes[ATTR_BACKUP_STAGE] is None
    assert state.attributes[ATTR_FAILED_REASON] == "unknown_error"
