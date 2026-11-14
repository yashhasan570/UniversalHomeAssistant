"""Validate Yardian switch behavior."""

from unittest.mock import AsyncMock, patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from pyyardian import NetworkException
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.components.yardian.coordinator import SCAN_INTERVAL
from universalassistant.const import (
    STATE_ON,
    STATE_UNAVAILABLE,
    CommonServiceArgument,
    Platform,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_all_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.yardian.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_turn_on_switch(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test turning on a switch."""
    await setup_integration(hass, mock_config_entry)

    entity_id = "switch.zone_1"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    mock_yardian_client.start_irrigation.assert_called_once_with(0, 6)


async def test_turn_off_switch(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test turning off a switch."""
    await setup_integration(hass, mock_config_entry)

    entity_id = "switch.zone_1"
    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    mock_yardian_client.stop_zone.assert_called_once()


@pytest.mark.usefixtures("switch_platform_only")
async def test_switch_unavailable_on_failed_update(
    hass: UniversalAssistant,
    mock_yardian_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test a switch becomes unavailable when an update fails."""
    await setup_integration(hass, mock_config_entry)

    entity_id = "switch.zone_1"

    assert hass.states.get(entity_id).state == STATE_ON

    mock_yardian_client.fetch_device_state.side_effect = NetworkException
    freezer.tick(SCAN_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)

    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE

    mock_yardian_client.fetch_device_state.side_effect = None
    freezer.tick(SCAN_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)

    assert hass.states.get(entity_id).state == STATE_ON
