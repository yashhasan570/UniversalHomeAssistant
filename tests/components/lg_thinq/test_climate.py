"""Tests for the LG Thinq climate platform."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.climate import (
    ATTR_FAN_MODE,
    DOMAIN as CLIMATE_DOMAIN,
    SERVICE_SET_FAN_MODE,
    ClimateService,
)
from universalassistant.const import ATTR_ENTITY_ID, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er
from universalassistant.util.unit_system import US_CUSTOMARY_SYSTEM

from . import setup_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    "device_fixture", ["air_conditioner", "air_conditioner1", "air_conditioner2"]
)
async def test_climate_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    devices: AsyncMock,
    mock_thinq_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    hass.config.units = US_CUSTOMARY_SYSTEM
    with patch("universalassistant.components.lg_thinq.PLATFORMS", [Platform.CLIMATE]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("device_fixture", "entity_id", "service", "service_data", "expected_value"),
    [
        (
            "air_conditioner",
            "climate.test_air_conditioner",
            SERVICE_SET_FAN_MODE,
            {ATTR_FAN_MODE: "auto"},
            "auto",
        ),
        (
            "air_conditioner1",
            "climate.test_air_conditioner1",
            SERVICE_SET_FAN_MODE,
            {ATTR_FAN_MODE: "auto"},
            "nature",
        ),
    ],
)
async def test_fan_mode_service_calls(
    hass: UniversalAssistant,
    devices: AsyncMock,
    mock_thinq_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    service: str,
    entity_id: str,
    service_data: dict,
    expected_value: str,
) -> None:
    """Test fan_mode service calls send the correct fan mode values."""
    with patch("universalassistant.components.lg_thinq.PLATFORMS", [Platform.CLIMATE]):
        await setup_integration(hass, mock_config_entry)

    coordinator = next(iter(mock_config_entry.runtime_data.coordinators.values()))
    coordinator.api.async_set_fan_mode = AsyncMock()

    await hass.services.async_call(
        CLIMATE_DOMAIN,
        service,
        {ATTR_ENTITY_ID: entity_id, **service_data},
        blocking=True,
    )

    coordinator.api.async_set_fan_mode.assert_awaited_once_with(
        "climate_air_conditioner", expected_value
    )


@pytest.mark.parametrize("device_fixture", ["air_conditioner"])
@pytest.mark.usefixtures("devices")
async def test_service_call_connection_error_raises_universal_assistant_error(
    hass: UniversalAssistant,
    mock_thinq_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test a network error during a service call raises UniversalAssistantError."""
    with patch("universalassistant.components.lg_thinq.PLATFORMS", [Platform.CLIMATE]):
        await setup_integration(hass, mock_config_entry)

    mock_thinq_api.async_post_device_control.side_effect = TimeoutError

    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            ClimateService.SET_FAN_MODE,
            {TargetKey.ENTITY_ID: "climate.test_air_conditioner", "fan_mode": "low"},
            blocking=True,
        )
