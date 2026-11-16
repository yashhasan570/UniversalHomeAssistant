"""Test GitHub sensor."""

from unittest.mock import AsyncMock, patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.github.const import FALLBACK_UPDATE_INTERVAL
from universalassistant.const import STATE_UNAVAILABLE, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration

TEST_SENSOR_ENTITY = "sensor.octocat_hello_world_latest_release"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: UniversalAssistant,
    github_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.github.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_sensor_updates_with_empty_release_array(
    hass: UniversalAssistant,
    github_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the sensor updates by default GitHub sensors."""
    await setup_integration(hass, mock_config_entry)
    state = hass.states.get(TEST_SENSOR_ENTITY)
    assert state.state == "v1.0.0"

    github_client.graphql.return_value.data["data"]["repository"]["release"] = None

    freezer.tick(FALLBACK_UPDATE_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    new_state = hass.states.get(TEST_SENSOR_ENTITY)
    assert new_state.state == STATE_UNAVAILABLE


async def test_latest_release_downloads_without_assets(
    hass: UniversalAssistant,
    github_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the downloads sensor is unavailable when the release has no assets."""
    release = github_client.graphql.return_value.data["data"]["repository"]["release"]
    release["assets"]["nodes"] = []
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("sensor.octocat_hello_world_latest_release_downloads")
    assert state.state == STATE_UNAVAILABLE
