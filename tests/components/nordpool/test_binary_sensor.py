"""The test for the Nord Pool binary sensor platform."""

from datetime import timedelta
from http import HTTPStatus

from freezegun.api import FrozenDateTimeFactory
from pynordpool import API
import pytest
from pytest_universalassistant.common import async_fire_time_changed, snapshot_platform
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.mark.freeze_time("2025-10-01T18:00:00+00:00")
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.BINARY_SENSOR]],
)
async def test_binary_sensor_on(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Nord Pool sensor."""

    await snapshot_platform(hass, entity_registry, snapshot, load_int.entry_id)


@pytest.mark.freeze_time("2025-10-01T18:00:00+00:00")
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.BINARY_SENSOR]],
)
async def test_binary_sensor_off(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    aioclient_mock: AiohttpClientMocker,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the Nord Pool sensor."""

    aioclient_mock.request(
        "GET",
        url=API + "/DayAheadPrices",
        params={
            "date": "2025-10-03",
            "market": "DayAhead",
            "deliveryArea": "SE3,SE4",
            "currency": "SEK",
        },
        status=HTTPStatus.NO_CONTENT,
    )

    freezer.tick(timedelta(days=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)

    await snapshot_platform(hass, entity_registry, snapshot, load_int.entry_id)
