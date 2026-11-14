"""Test the my-PV select platform."""

from unittest.mock import AsyncMock, Mock, patch

from my_pv.exceptions import (
    MyPVAuthenticationError,
    MyPVConnectionError,
    MyPVTooManyRequestsError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import STATE_UNAVAILABLE, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed, __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_integration

pytestmark = pytest.mark.usefixtures("entity_registry_enabled_by_default")


@pytest.mark.usefixtures("mock_my_pv_client")
async def test_select(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test successful setup of the select platform."""
    with patch("universalassistant.components.my_pv.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_select_unavailable_not_connected(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test if a select is unavailable when not connected."""
    mock_my_pv_client.connected = False

    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == STATE_UNAVAILABLE


async def test_select_unavailable_setup_value_none(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test if a select is unavailable when setup value is None."""
    mock_my_pv_client.get_setup_value = Mock(return_value=None)

    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == STATE_UNAVAILABLE


async def test_select_select_option(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test setting value."""
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == "0"

    mock_my_pv_client.get_setup_value = Mock(return_value="1")

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.my_pv_ac_elwa_2_boost_mode",
            SelectServiceArgument.OPTION: "1",
        },
        blocking=True,
    )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bstmode", "1")

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == "1"


async def test_select_select_option_returns_false(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test for __HAC_KEEP__Error when set_setup_value returns false."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.set_setup_value.return_value = False

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.my_pv_ac_elwa_2_boost_mode",
                SelectServiceArgument.OPTION: "1",
            },
            blocking=True,
        )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bstmode", "1")

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == "0"


@pytest.mark.parametrize(
    ("error", "expected_ha_error"),
    [
        (MyPVConnectionError(), __HAC_KEEP__Error),
        (MyPVAuthenticationError(), ConfigEntryAuthFailed),
        (MyPVTooManyRequestsError(), __HAC_KEEP__Error),
    ],
)
async def test_select_select_option_raises_error(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
    error: MyPVConnectionError | MyPVAuthenticationError,
    expected_ha_error: type[__HAC_KEEP__Error],
) -> None:
    """Test for __HAC_KEEP__Error when set_setup_value raises error."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.set_setup_value.side_effect = error

    with pytest.raises(expected_ha_error):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.my_pv_ac_elwa_2_boost_mode",
                SelectServiceArgument.OPTION: "1",
            },
            blocking=True,
        )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bstmode", "1")

    state = hass.states.get("select.my_pv_ac_elwa_2_boost_mode")
    assert state.state == "0"
