"""Tests for Bosch Alarm component."""

import asyncio
from collections.abc import AsyncGenerator
import datetime as dt
from unittest.mock import AsyncMock, patch

import probatio
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.bosch_alarm.const import DOMAIN
from universalassistant.components.bosch_alarm.services import (
    BoschAlarmService,
    BoschAlarmServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util

from . import setup_integration


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("universalassistant.components.bosch_alarm.PLATFORMS", []):
        yield


async def test_set_date_time_service(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls succeed if the service call is valid."""
    await setup_integration(hass, mock_config_entry)
    await hass.services.async_call(
        DOMAIN,
        BoschAlarmService.SET_DATE_TIME,
        {
            CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
            BoschAlarmServiceArgument.DATETIME: dt_util.now(),
        },
        blocking=True,
    )
    mock_panel.set_panel_date.assert_called_once()


async def test_set_date_time_service_fails_bad_entity(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if done for an incorrect entity."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: "bad-config_id",
                BoschAlarmServiceArgument.DATETIME: dt_util.now(),
            },
            blocking=True,
        )
    assert err.value.translation_key == "service_config_entry_not_found"
    assert err.value.translation_placeholders["entry_id"] == "bad-config_id"


async def test_set_date_time_service_fails_bad_params(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if done with incorrect params."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(
        probatio.MultipleInvalid,
        match=r"Invalid datetime specified:  at 'datetime'",
    ):
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                BoschAlarmServiceArgument.DATETIME: "",
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_bad_year_before(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(
        probatio.MultipleInvalid,
        match=r"datetime must be before 2038 at 'datetime'",
    ):
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                BoschAlarmServiceArgument.DATETIME: dt.datetime(2038, 1, 1),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_bad_year_after(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    mock_panel.set_panel_date.side_effect = ValueError()
    with pytest.raises(
        probatio.MultipleInvalid,
        match=r"datetime must be after 2009 at 'datetime'",
    ):
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                BoschAlarmServiceArgument.DATETIME: dt.datetime(2009, 1, 1),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_connection_error(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    mock_panel.set_panel_date.side_effect = asyncio.InvalidStateError()
    with pytest.raises(
        __HAC_KEEP__Error,
        match=f'Could not connect to "{mock_config_entry.title}"',
    ):
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                BoschAlarmServiceArgument.DATETIME: dt_util.now(),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_unloaded(
    hass: __HAC_KEEP__,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the config entry is unloaded."""
    await async_setup_component(hass, DOMAIN, {})
    mock_config_entry.add_to_hass(hass)
    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            BoschAlarmService.SET_DATE_TIME,
            {
                CommonServiceArgument.CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                BoschAlarmServiceArgument.DATETIME: dt_util.now(),
            },
            blocking=True,
        )
    assert err.value.translation_key == "service_config_entry_not_loaded"
    assert err.value.translation_placeholders["entry_title"] == "Mock Title"
