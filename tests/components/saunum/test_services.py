"""Tests for Saunum services."""

from dataclasses import replace
from unittest.mock import MagicMock

from pysaunum import SaunumException
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.saunum.const import DOMAIN
from universalassistant.components.saunum.services import (
    LeilSaunaService,
    LeilSaunaServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to specify platforms to test."""
    return [Platform.CLIMATE]


async def test_start_session_success(
    hass: UniversalAssistant,
    init_integration: MockConfigEntry,
    mock_saunum_client: MagicMock,
) -> None:
    """Test start_session service success."""
    await hass.services.async_call(
        DOMAIN,
        LeilSaunaService.START_SESSION,
        {
            CommonServiceArgument.ENTITY_ID: "climate.saunum_leil",
            LeilSaunaServiceArgument.DURATION: {"hours": 2, "minutes": 0, "seconds": 0},
            LeilSaunaServiceArgument.TARGET_TEMPERATURE: 80,
            LeilSaunaServiceArgument.FAN_DURATION: {"minutes": 10},
        },
        blocking=True,
    )

    mock_saunum_client.async_set_sauna_duration.assert_called_once_with(120)
    mock_saunum_client.async_set_target_temperature.assert_called_once_with(80)
    mock_saunum_client.async_set_fan_duration.assert_called_once_with(10)
    mock_saunum_client.async_start_session.assert_called_once()


async def test_start_session_with_defaults(
    hass: UniversalAssistant,
    init_integration: MockConfigEntry,
    mock_saunum_client: MagicMock,
) -> None:
    """Test start_session service uses defaults when optional fields omitted."""
    await hass.services.async_call(
        DOMAIN,
        LeilSaunaService.START_SESSION,
        {CommonServiceArgument.ENTITY_ID: "climate.saunum_leil"},
        blocking=True,
    )

    # Defaults: duration=120, target_temperature=80, fan_duration=10
    mock_saunum_client.async_set_sauna_duration.assert_called_once_with(120)
    mock_saunum_client.async_set_target_temperature.assert_called_once_with(80)
    mock_saunum_client.async_set_fan_duration.assert_called_once_with(10)
    mock_saunum_client.async_start_session.assert_called_once()


async def test_start_session_door_open(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_saunum_client: MagicMock,
) -> None:
    """Test start_session service fails when door is open."""
    mock_saunum_client.async_get_data.return_value = replace(
        mock_saunum_client.async_get_data.return_value, door_open=True
    )
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            DOMAIN,
            LeilSaunaService.START_SESSION,
            {CommonServiceArgument.ENTITY_ID: "climate.saunum_leil"},
            blocking=True,
        )

    assert exc_info.value.translation_key == "door_open"


async def test_start_session_communication_error(
    hass: UniversalAssistant,
    init_integration: MockConfigEntry,
    mock_saunum_client: MagicMock,
) -> None:
    """Test start_session service handles communication error."""
    mock_saunum_client.async_set_sauna_duration.side_effect = SaunumException(
        "Connection lost"
    )

    with pytest.raises(UniversalAssistantError) as exc_info:
        await hass.services.async_call(
            DOMAIN,
            LeilSaunaService.START_SESSION,
            {CommonServiceArgument.ENTITY_ID: "climate.saunum_leil"},
            blocking=True,
        )

    assert exc_info.value.translation_key == "start_session_failed"
