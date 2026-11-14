"""Tests for the button module."""

from datetime import timedelta
from typing import Any
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from pyvesync.utils.errors import VeSyncAPIResponseError
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er
from universalassistant.helpers.update_coordinator import REQUEST_REFRESH_DEFAULT_COOLDOWN

from .common import mock_devices_response

ENTITY_RESET_FILTER = "button.air_purifier_200s_reset_filter"
RESET_FILTER = "pyvesync.devices.vesyncpurifier.VeSyncAirBypass.reset_filter"
UPDATE_ALL_DEVICES = "pyvesync.vesync.VeSync.update_all_devices"


async def test_button_state(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test the resulting setup state is as expected for the platform."""

    mock_devices_response(aioclient_mock, "Air Purifier 200s")

    with patch("universalassistant.components.vesync.PLATFORMS", [Platform.BUTTON]):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_reset_filter(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    aioclient_mock: AiohttpClientMocker,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test pressing the reset filter button resets the filter and refreshes."""

    mock_devices_response(aioclient_mock, "Air Purifier 200s")

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    with (
        patch(RESET_FILTER, return_value=True) as method_mock,
        patch(UPDATE_ALL_DEVICES) as update_mock,
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: ENTITY_RESET_FILTER},
            blocking=True,
        )

        freezer.tick(timedelta(seconds=REQUEST_REFRESH_DEFAULT_COOLDOWN))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    method_mock.assert_called_once()
    update_mock.assert_called_once()


@pytest.mark.parametrize(
    "reset_filter",
    [
        {"return_value": False},
        {"side_effect": VeSyncAPIResponseError("API error")},
    ],
    ids=["returns_false", "raises"],
)
async def test_reset_filter_raises_error(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    aioclient_mock: AiohttpClientMocker,
    freezer: FrozenDateTimeFactory,
    reset_filter: dict[str, Any],
) -> None:
    """Test a failed filter reset raises __HAC_KEEP__Error and skips the refresh."""

    mock_devices_response(aioclient_mock, "Air Purifier 200s")

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    with (
        patch(RESET_FILTER, **reset_filter) as method_mock,
        patch(UPDATE_ALL_DEVICES) as update_mock,
    ):
        with pytest.raises(
            __HAC_KEEP__Error, match="Invalid response from the VeSync API"
        ):
            await hass.services.async_call(
                BUTTON_DOMAIN,
                ButtonService.PRESS,
                {CommonServiceArgument.ENTITY_ID: ENTITY_RESET_FILTER},
                blocking=True,
            )

        freezer.tick(timedelta(seconds=REQUEST_REFRESH_DEFAULT_COOLDOWN))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    method_mock.assert_called_once()
    update_mock.assert_not_called()
