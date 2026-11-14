"""Tests for the AirGradient switch platform."""

from datetime import timedelta
from unittest.mock import AsyncMock, patch

from airgradient import AirGradientConnectionError, AirGradientError, ApiVersion
from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import ATTR_ENTITY_ID, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import async_load_config_fixture, load_config_fixture, setup_integration


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.airgradient.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_setting_value(
    hass: __HAC_KEEP__,
    mock_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting value."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        target={ATTR_ENTITY_ID: "switch.airgradient_post_data_to_airgradient"},
        blocking=True,
    )
    mock_airgradient_client.enable_sharing_data.assert_called_once()
    mock_airgradient_client.enable_sharing_data.reset_mock()

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        target={ATTR_ENTITY_ID: "switch.airgradient_post_data_to_airgradient"},
        blocking=True,
    )
    mock_airgradient_client.enable_sharing_data.assert_called_once()


async def test_v1_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_v1_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test V1 switch entities."""
    mock_v1_airgradient_client.get_config.return_value = load_config_fixture(
        "config_v1_local.json", ApiVersion.V1
    )
    with patch("universalassistant.components.airgradient.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "method"),
    [
        ("switch.airgradient_buzzer", "set_buzzer_enabled"),
        ("switch.airgradient_cloud_connection", "set_cloud_connection"),
    ],
)
async def test_v1_switch_writes(
    hass: __HAC_KEEP__,
    mock_v1_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    method: str,
) -> None:
    """Test V1 switch writes."""
    mock_v1_airgradient_client.get_config.return_value = load_config_fixture(
        "config_v1_local.json", ApiVersion.V1
    )
    with patch("universalassistant.components.airgradient.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        target={ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    getattr(mock_v1_airgradient_client, method).assert_awaited_once_with(False)


async def test_cloud_creates_no_switch(
    hass: __HAC_KEEP__,
    mock_cloud_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test cloud configuration control."""
    with patch("universalassistant.components.airgradient.PLATFORMS", [Platform.SWITCH]):
        await setup_integration(hass, mock_config_entry)

    assert len(hass.states.async_all()) == 0

    mock_cloud_airgradient_client.get_config.return_value = (
        await async_load_config_fixture(hass, "get_config_local.json")
    )

    freezer.tick(timedelta(minutes=5))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert len(hass.states.async_all()) == 1

    mock_cloud_airgradient_client.get_config.return_value = (
        await async_load_config_fixture(hass, "get_config_cloud.json")
    )

    freezer.tick(timedelta(minutes=5))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert len(hass.states.async_all()) == 0


@pytest.mark.parametrize(
    ("exception", "error_message"),
    [
        (
            AirGradientConnectionError("Something happened"),
            "An error occurred while communicating with the"
            " Airgradient device: Something happened",
        ),
        (
            AirGradientError("Something else happened"),
            "An unknown error occurred while communicating"
            " with the Airgradient device:"
            " Something else happened",
        ),
    ],
)
async def test_exception_handling(
    hass: __HAC_KEEP__,
    mock_airgradient_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    exception: Exception,
    error_message: str,
) -> None:
    """Test exception handling."""
    await setup_integration(hass, mock_config_entry)

    mock_airgradient_client.enable_sharing_data.side_effect = exception
    with pytest.raises(__HAC_KEEP__Error, match=error_message):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            target={ATTR_ENTITY_ID: "switch.airgradient_post_data_to_airgradient"},
            blocking=True,
        )
