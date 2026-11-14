"""Test the Seafile number platform."""

import dataclasses
from unittest.mock import AsyncMock, patch

from aioseafile import SeafileConnectionError
from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.components.seafile.coordinator import UPDATE_INTERVAL
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
from .conftest import LIBRARY_ID

HISTORY = "select.documents_history"
HISTORY_DAYS = "number.documents_history_days"


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all number entities."""
    mock_seafile_client.get_library_history_limit.return_value = 45
    with patch("universalassistant.components.seafile.PLATFORMS", [Platform.NUMBER]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    "keep_days",
    [
        pytest.param(-1, id="keep_all"),
        pytest.param(0, id="keep_none"),
    ],
)
async def test_unavailable_without_period(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    keep_days: int,
) -> None:
    """Test the days are unavailable when the library doesn't keep a period."""
    mock_seafile_client.get_library_history_limit.return_value = keep_days
    await setup_integration(hass, mock_config_entry)

    assert (state := hass.states.get(HISTORY_DAYS))
    assert state.state == STATE_UNAVAILABLE


async def test_set_value(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting the days of history to keep."""
    mock_seafile_client.get_library_history_limit.return_value = 45
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: HISTORY_DAYS,
            NumberServiceArgument.VALUE: 90,
        },
        blocking=True,
    )

    mock_seafile_client.set_library_history_limit.assert_awaited_once_with(
        LIBRARY_ID, 90
    )
    assert (state := hass.states.get(HISTORY_DAYS))
    assert state.state == "90"


async def test_set_value_error(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test a failed change is raised as a translated error."""
    mock_seafile_client.get_library_history_limit.return_value = 45
    await setup_integration(hass, mock_config_entry)
    mock_seafile_client.set_library_history_limit.side_effect = SeafileConnectionError

    with pytest.raises(__HAC_KEEP__Error) as exc_info:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: HISTORY_DAYS,
                NumberServiceArgument.VALUE: 90,
            },
            blocking=True,
        )
    assert exc_info.value.translation_key == "api_error"
    assert (state := hass.states.get(HISTORY_DAYS))
    assert state.state == "45"


@pytest.mark.parametrize(
    ("keep_days", "option", "days_state"),
    [
        pytest.param(-1, "limited", "30", id="to_limited"),
        pytest.param(45, "keep_all", STATE_UNAVAILABLE, id="to_keep_all"),
    ],
)
async def test_follows_history_select(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    keep_days: int,
    option: str,
    days_state: str,
) -> None:
    """Test the days update right away when the history mode changes."""
    mock_seafile_client.get_library_history_limit.return_value = keep_days
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: HISTORY,
            SelectServiceArgument.OPTION: option,
        },
        blocking=True,
    )

    assert (state := hass.states.get(HISTORY_DAYS))
    assert state.state == days_state


async def test_no_number_for_shared_library(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test a library shared with the account without admin rights has no days."""
    mock_seafile_client.get_libraries.return_value = [
        dataclasses.replace(library, type="srepo", permission="rw")
        for library in mock_seafile_client.get_libraries.return_value
    ]
    await setup_integration(hass, mock_config_entry)

    assert hass.states.get(HISTORY_DAYS) is None


async def test_number_added_when_shared_as_admin(
    hass: __HAC_KEEP__,
    mock_seafile_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the days are added once the library is shared with the account as admin."""
    mock_seafile_client.get_library_history_limit.return_value = 45
    libraries = mock_seafile_client.get_libraries.return_value
    mock_seafile_client.get_libraries.return_value = [
        dataclasses.replace(library, type="srepo", permission="rw")
        for library in libraries
    ]
    await setup_integration(hass, mock_config_entry)
    assert hass.states.get(HISTORY_DAYS) is None

    mock_seafile_client.get_libraries.return_value = [
        dataclasses.replace(library, type="srepo", permission="admin")
        for library in libraries
    ]
    freezer.tick(UPDATE_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)

    assert (state := hass.states.get(HISTORY_DAYS))
    assert state.state == "45"
