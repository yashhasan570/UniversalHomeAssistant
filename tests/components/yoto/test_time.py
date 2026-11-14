"""Tests for the Yoto time platform."""

from datetime import time
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion
from yoto_api import YotoError

from universalassistant.components.time import (
    DOMAIN as TIME_DOMAIN,
    TimeService,
    TimeServiceArgument,
)
from universalassistant.const import STATE_UNAVAILABLE, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration
from .conftest import PLAYER_ID

pytestmark = pytest.mark.usefixtures("setup_credentials")


async def _setup(hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry) -> None:
    """Set up the integration with only the time platform."""
    with patch("universalassistant.components.yoto.PLATFORMS", [Platform.TIME]):
        await setup_integration(hass, mock_config_entry)


@pytest.mark.usefixtures("mock_yoto_client")
async def test_all_entities(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot every Yoto time entity."""
    await _setup(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_available_when_offline(
    hass: __HAC_KEEP__,
    mock_yoto_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Config is written over REST, so entities stay available when offline."""
    player = next(iter(mock_yoto_client.players.values()))
    player.is_online = False

    await _setup(hass, mock_config_entry)

    state = hass.states.get("time.nursery_yoto_day_mode_start")
    assert state is not None
    assert state.state != STATE_UNAVAILABLE


@pytest.mark.parametrize(
    ("entity_id", "expected_fields"),
    [
        pytest.param(
            "time.nursery_yoto_day_mode_start",
            {"day_time": time(8, 30)},
            id="day-mode-start",
        ),
        pytest.param(
            "time.nursery_yoto_night_mode_start",
            {"night_time": time(8, 30)},
            id="night-mode-start",
        ),
    ],
)
async def test_set_value(
    hass: __HAC_KEEP__,
    mock_yoto_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    expected_fields: dict[str, time],
) -> None:
    """Setting a time writes the matching player config field."""
    await _setup(hass, mock_config_entry)

    await hass.services.async_call(
        TIME_DOMAIN,
        TimeService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            TimeServiceArgument.TIME: time(8, 30),
        },
        blocking=True,
    )

    mock_yoto_client.set_player_config.assert_awaited_once_with(
        PLAYER_ID, **expected_fields
    )
    mock_yoto_client.update_player_info.assert_awaited_once_with(PLAYER_ID)


async def test_set_value_failure(
    hass: __HAC_KEEP__,
    mock_yoto_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """A failed config write raises a __HA_KEEP__ error."""
    await _setup(hass, mock_config_entry)
    mock_yoto_client.set_player_config.side_effect = YotoError("MQTT timeout")

    with pytest.raises(
        __HAC_KEEP__Error, match="Failed to update Yoto player settings"
    ):
        await hass.services.async_call(
            TIME_DOMAIN,
            TimeService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "time.nursery_yoto_day_mode_start",
                TimeServiceArgument.TIME: time(7, 0),
            },
            blocking=True,
        )
