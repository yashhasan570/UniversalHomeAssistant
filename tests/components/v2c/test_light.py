"""Test the V2C light platform."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.light import (
    DOMAIN as LIGHT_DOMAIN,
    LightService,
    LightServiceArgument,
)
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_light(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test states of the light entities."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_light_turn_on_off(
    hass: UniversalAssistant,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test turning light entities on and off."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    await hass.services.async_call(
        LIGHT_DOMAIN,
        LightService.TURN_ON,
        {TargetKey.ENTITY_ID: "light.evse_1_1_1_1_light_led"},
        blocking=True,
    )

    mock_v2c_client.light_led.assert_called_once_with(100)

    await hass.services.async_call(
        LIGHT_DOMAIN,
        LightService.TURN_OFF,
        {TargetKey.ENTITY_ID: "light.evse_1_1_1_1_logo_led"},
        blocking=True,
    )

    mock_v2c_client.logo_led.assert_called_once_with(0)


async def test_logo_led_set_brightness(
    hass: UniversalAssistant,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting Logo LED brightness."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    await hass.services.async_call(
        LIGHT_DOMAIN,
        LightService.TURN_ON,
        {
            TargetKey.ENTITY_ID: "light.evse_1_1_1_1_logo_led",
            LightServiceArgument.BRIGHTNESS: 128,
        },
        blocking=True,
    )

    mock_v2c_client.logo_led.assert_called_once_with(50)


async def test_logo_led_set_low_brightness(
    hass: UniversalAssistant,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting Logo LED low brightness."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    await hass.services.async_call(
        LIGHT_DOMAIN,
        LightService.TURN_ON,
        {
            TargetKey.ENTITY_ID: "light.evse_1_1_1_1_logo_led",
            LightServiceArgument.BRIGHTNESS: 1,
        },
        blocking=True,
    )

    mock_v2c_client.logo_led.assert_called_once_with(1)


async def test_light_led_disabled_by_default(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test Light LED entity is disabled by default."""

    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    entity_id = "light.evse_1_1_1_1_light_led"
    entry = entity_registry.async_get(entity_id)
    assert entry is not None
    assert entry.disabled_by is er.RegistryEntryDisabler.INTEGRATION
    assert hass.states.get(entity_id) is None


@pytest.mark.parametrize(
    ("field", "entity_id"),
    [
        ("light_led", "light.evse_1_1_1_1_light_led"),
        ("logo_led", "light.evse_1_1_1_1_logo_led"),
    ],
)
async def test_led_not_created_when_missing(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    field: str,
    entity_id: str,
) -> None:
    """Test missing LED entities are not created."""
    setattr(mock_v2c_client.get_data.return_value, field, None)

    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    assert entity_registry.async_get(entity_id) is None
    assert hass.states.get(entity_id) is None


async def test_logo_led_enabled_when_present(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test Logo LED entity is enabled when supported."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.LIGHT]):
        await init_integration(hass, mock_config_entry)

    entity_id = "light.evse_1_1_1_1_logo_led"
    entry = entity_registry.async_get(entity_id)
    assert entry is not None
    assert entry.disabled_by is None
    assert hass.states.get(entity_id) is not None
