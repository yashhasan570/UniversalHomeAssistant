"""Test the my-PV number platform."""

from unittest.mock import AsyncMock, Mock, patch

from my_pv.exceptions import (
    MyPVAuthenticationError,
    MyPVConnectionError,
    MyPVTooManyRequestsError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import STATE_UNAVAILABLE, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration

pytestmark = pytest.mark.usefixtures("entity_registry_enabled_by_default")


@pytest.mark.usefixtures("mock_my_pv_client")
async def test_number(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test successful setup of the number platform."""
    with patch("universalassistant.components.my_pv.PLATFORMS", [Platform.NUMBER]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_number_unavailable_not_connected(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test if a number is unavailable when not connected."""
    mock_my_pv_client.connected = False

    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == STATE_UNAVAILABLE


async def test_number_unavailable_setup_value_none(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test if a number is unavailable when setup value is None."""
    mock_my_pv_client.get_setup_value = Mock(return_value=None)

    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == STATE_UNAVAILABLE


async def test_number_set_value(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test setting value."""
    await setup_integration(hass, mock_config_entry)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == "55.0"

    mock_my_pv_client.get_setup_value = Mock(return_value=70.0)

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            TargetKey.ENTITY_ID: "number.my_pv_ac_elwa_2_boost_target_temperature",
            NumberServiceArgument.VALUE: 70.0,
        },
        blocking=True,
    )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bsttemp", 70.0)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == "70.0"


async def test_number_set_value_returns_false(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
) -> None:
    """Test for UniversalAssistantError when set_setup_value returns false."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.set_setup_value.return_value = False

    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                TargetKey.ENTITY_ID: "number.my_pv_ac_elwa_2_boost_target_temperature",
                NumberServiceArgument.VALUE: 70,
            },
            blocking=True,
        )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bsttemp", 70)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == "55.0"


@pytest.mark.parametrize(
    ("error", "expected_ha_error"),
    [
        (MyPVConnectionError(), UniversalAssistantError),
        (MyPVAuthenticationError(), ConfigEntryAuthFailed),
        (MyPVTooManyRequestsError(), UniversalAssistantError),
    ],
)
async def test_number_set_value_raises_error(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_my_pv_client: AsyncMock,
    error: MyPVConnectionError | MyPVAuthenticationError,
    expected_ha_error: type[UniversalAssistantError],
) -> None:
    """Test for UniversalAssistantError when set_setup_value raises error."""
    await setup_integration(hass, mock_config_entry)

    mock_my_pv_client.set_setup_value.side_effect = error

    with pytest.raises(expected_ha_error):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                TargetKey.ENTITY_ID: "number.my_pv_ac_elwa_2_boost_target_temperature",
                NumberServiceArgument.VALUE: 70,
            },
            blocking=True,
        )
    mock_my_pv_client.set_setup_value.assert_awaited_once_with("bsttemp", 70)

    state = hass.states.get("number.my_pv_ac_elwa_2_boost_target_temperature")
    assert state.state == "55.0"
