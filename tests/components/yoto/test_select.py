"""Tests for the Yoto select platform."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion
from yoto_api import YotoError

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import STATE_UNAVAILABLE, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration
from .conftest import PLAYER_ID

pytestmark = pytest.mark.usefixtures("setup_credentials")


async def _setup(hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry) -> None:
    """Set up the integration with only the select platform."""
    with patch("universalassistant.components.yoto.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)


@pytest.mark.usefixtures("mock_yoto_client")
async def test_all_entities(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot every Yoto select entity."""
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

    state = hass.states.get("select.nursery_yoto_day_mode_color")
    assert state is not None
    assert state.state != STATE_UNAVAILABLE


@pytest.mark.parametrize(
    ("entity_id", "expected_fields"),
    [
        pytest.param(
            "select.nursery_yoto_day_mode_color",
            {"day_ambient_preset": "sky_blue"},
            id="day-mode-color",
        ),
        pytest.param(
            "select.nursery_yoto_night_mode_color",
            {"night_ambient_preset": "sky_blue"},
            id="night-mode-color",
        ),
    ],
)
async def test_select_option(
    hass: __HAC_KEEP__,
    mock_yoto_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    expected_fields: dict[str, str],
) -> None:
    """Selecting a preset writes the matching player config field."""
    await _setup(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            SelectServiceArgument.OPTION: "sky_blue",
        },
        blocking=True,
    )

    mock_yoto_client.set_player_config.assert_awaited_once_with(
        PLAYER_ID, **expected_fields
    )
    mock_yoto_client.update_player_info.assert_awaited_once_with(PLAYER_ID)


async def test_select_option_failure(
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
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.nursery_yoto_day_mode_color",
                SelectServiceArgument.OPTION: "sky_blue",
            },
            blocking=True,
        )
