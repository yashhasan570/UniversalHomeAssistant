"""Tests for the Rainforest RAVEn sensors."""

from datetime import timedelta
from unittest.mock import AsyncMock

from aioraven.device import RAVEnConnectionError
from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_UNAVAILABLE
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .const import NETWORK_INFO


@pytest.mark.usefixtures("mock_entry")
async def test_sensors(
    hass: __HAC_KEEP__,
    mock_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the sensors."""
    assert len(hass.states.async_all()) == 5

    await snapshot_platform(hass, entity_registry, snapshot, mock_entry.entry_id)


@pytest.mark.usefixtures("mock_entry")
async def test_device_update_error(
    hass: __HAC_KEEP__,
    mock_device: AsyncMock,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test handling of a device error during an update."""
    mock_device.get_network_info.side_effect = (RAVEnConnectionError, NETWORK_INFO)

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state != STATE_UNAVAILABLE for state in states)

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state == STATE_UNAVAILABLE for state in states)

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state != STATE_UNAVAILABLE for state in states)


@pytest.mark.usefixtures("mock_entry")
async def test_device_update_timeout(
    hass: __HAC_KEEP__, mock_device: AsyncMock, freezer: FrozenDateTimeFactory
) -> None:
    """Test handling of a device timeout during an update."""
    mock_device.get_network_info.side_effect = (TimeoutError, NETWORK_INFO)

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state != STATE_UNAVAILABLE for state in states)

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state == STATE_UNAVAILABLE for state in states)

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)

    states = hass.states.async_all()
    assert len(states) == 5
    assert all(state.state != STATE_UNAVAILABLE for state in states)


@pytest.mark.usefixtures("mock_entry")
async def test_device_cache(
    hass: __HAC_KEEP__, mock_device: AsyncMock, freezer: FrozenDateTimeFactory
) -> None:
    """Test that the device isn't re-opened for subsequent refreshes."""
    assert mock_device.get_network_info.call_count == 1
    assert mock_device.open.call_count == 1

    freezer.tick(timedelta(seconds=60))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_device.get_network_info.call_count == 2
    assert mock_device.open.call_count == 1
