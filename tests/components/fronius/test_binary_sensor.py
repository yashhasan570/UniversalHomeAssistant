"""Tests for the Fronius binary sensor platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import snapshot_platform
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import MOCK_UID, mock_responses, setup_fronius_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    ("fixture_set", "unique_id"),
    [
        pytest.param("gen24", MOCK_UID, id="gen24"),
        pytest.param("gen24_storage", "12345678", id="gen24_storage"),
    ],
)
async def test_binary_sensors(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    fixture_set: str,
    unique_id: str,
) -> None:
    """Test Fronius power flow binary sensors for Gen24 devices."""
    mock_responses(aioclient_mock, fixture_set=fixture_set)
    with patch("universalassistant.components.fronius.PLATFORMS", [Platform.BINARY_SENSOR]):
        config_entry = await setup_fronius_integration(
            hass, is_logger=False, unique_id=unique_id
        )

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_no_binary_sensors_without_backup_keys(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test that no binary sensors are created when the API omits the keys."""
    # The Symo power flow response has neither BackupMode nor BatteryStandby.
    mock_responses(aioclient_mock, fixture_set="symo")
    await setup_fronius_integration(hass, is_logger=True)

    assert not hass.states.async_all(domain_filter=BINARY_SENSOR_DOMAIN)
