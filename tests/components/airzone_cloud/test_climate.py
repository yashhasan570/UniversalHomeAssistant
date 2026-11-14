"""The climate tests for the Airzone Cloud platform."""

from collections.abc import Generator
from unittest.mock import patch

from aioairzone_cloud.exceptions import AirzoneCloudError
import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.climate import (
    ATTR_FAN_MODE,
    ATTR_HVAC_MODE,
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    DOMAIN as CLIMATE_DOMAIN,
    FAN_AUTO,
    FAN_LOW,
    SERVICE_SET_FAN_MODE,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_TEMPERATURE,
    ClimateEntityStateAttribute,
    HVACMode,
)
from universalassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from .util import async_init_integration


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("universalassistant.components.airzone_cloud.PLATFORMS", [Platform.CLIMATE]):
        yield


async def test_airzone_create_climates(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test creation of climates."""

    config_entry = await async_init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_airzone_climate_turn_on_off(hass: __HAC_KEEP__) -> None:
    """Test turning on/off."""

    await async_init_integration(hass)

    # Aidoos
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_ON,
            {
                ATTR_ENTITY_ID: "climate.bron",
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron")
    assert state.state == HVACMode.HEAT

    # Groups
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_ON,
            {
                ATTR_ENTITY_ID: "climate.group",
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.state == HVACMode.COOL

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_OFF,
            {
                ATTR_ENTITY_ID: "climate.group",
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.state == HVACMode.OFF

    # Installations
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_ON,
            {
                ATTR_ENTITY_ID: "climate.house",
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.state == HVACMode.COOL

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_OFF,
            {
                ATTR_ENTITY_ID: "climate.house",
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.state == HVACMode.OFF

    # Zones
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_ON,
            {
                ATTR_ENTITY_ID: "climate.dormitorio",
            },
            blocking=True,
        )

    state = hass.states.get("climate.dormitorio")
    assert state.state == HVACMode.COOL

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_TURN_OFF,
            {
                ATTR_ENTITY_ID: "climate.salon",
            },
            blocking=True,
        )

    state = hass.states.get("climate.salon")
    assert state.state == HVACMode.OFF


async def test_airzone_climate_set_fan_mode(hass: __HAC_KEEP__) -> None:
    """Test setting the fan mode."""

    await async_init_integration(hass)

    # Aidoos
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_FAN_MODE,
            {
                ATTR_ENTITY_ID: "climate.bron",
                ATTR_FAN_MODE: FAN_LOW,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron")
    assert state.attributes[ClimateEntityStateAttribute.FAN_MODE] == FAN_LOW

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_FAN_MODE,
            {
                ATTR_ENTITY_ID: "climate.bron_pro",
                ATTR_FAN_MODE: FAN_AUTO,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron_pro")
    assert state.attributes[ClimateEntityStateAttribute.FAN_MODE] == FAN_AUTO


async def test_airzone_climate_set_hvac_mode(hass: __HAC_KEEP__) -> None:
    """Test setting the HVAC mode."""

    await async_init_integration(hass)

    # Aidoos
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.bron",
                ATTR_HVAC_MODE: HVACMode.HEAT_COOL,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron")
    assert state.state == HVACMode.HEAT_COOL

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.bron",
                ATTR_HVAC_MODE: HVACMode.OFF,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron")
    assert state.state == HVACMode.OFF

    # Groups
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.group",
                ATTR_HVAC_MODE: HVACMode.DRY,
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.state == HVACMode.DRY

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.group",
                ATTR_HVAC_MODE: HVACMode.OFF,
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.state == HVACMode.OFF

    # Installations
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.house",
                ATTR_HVAC_MODE: HVACMode.DRY,
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.state == HVACMode.DRY

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.house",
                ATTR_HVAC_MODE: HVACMode.OFF,
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.state == HVACMode.OFF

    # Zones
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.salon",
                ATTR_HVAC_MODE: HVACMode.HEAT,
            },
            blocking=True,
        )

    state = hass.states.get("climate.salon")
    assert state.state == HVACMode.HEAT

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.salon",
                ATTR_HVAC_MODE: HVACMode.OFF,
            },
            blocking=True,
        )

    state = hass.states.get("climate.salon")
    assert state.state == HVACMode.OFF


async def test_airzone_climate_set_hvac_slave_error(hass: __HAC_KEEP__) -> None:
    """Test setting the HVAC mode for a slave zone."""

    await async_init_integration(hass)

    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
            return_value=None,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_HVAC_MODE,
            {
                ATTR_ENTITY_ID: "climate.dormitorio",
                ATTR_HVAC_MODE: HVACMode.HEAT,
            },
            blocking=True,
        )

    state = hass.states.get("climate.dormitorio")
    assert state.state == HVACMode.COOL


async def test_airzone_climate_set_temp(hass: __HAC_KEEP__) -> None:
    """Test setting the target temperature."""

    await async_init_integration(hass)

    # Groups
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.group",
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 20.5

    # Installations
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.house",
                ATTR_HVAC_MODE: HVACMode.HEAT,
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.state == HVACMode.HEAT
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 20.5

    # Zones
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.salon",
                ATTR_HVAC_MODE: HVACMode.HEAT,
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.salon")
    assert state.state == HVACMode.HEAT
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 20.5

    # Aidoo Pro with Double Setpoint
    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.bron_pro",
                ATTR_HVAC_MODE: HVACMode.HEAT_COOL,
                ATTR_TARGET_TEMP_HIGH: 25.0,
                ATTR_TARGET_TEMP_LOW: 20.0,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron_pro")
    assert state.state == HVACMode.HEAT_COOL
    assert state.attributes.get(ClimateEntityStateAttribute.TARGET_TEMP_HIGH) == 25.0
    assert state.attributes.get(ClimateEntityStateAttribute.TARGET_TEMP_LOW) == 20.0


async def test_airzone_climate_set_temp_error(hass: __HAC_KEEP__) -> None:
    """Test error when setting the target temperature."""

    await async_init_integration(hass)

    # Aidoos
    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
            side_effect=AirzoneCloudError,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.bron",
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.bron")
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 22.0

    # Groups
    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_group",
            side_effect=AirzoneCloudError,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.group",
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.group")
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 24.0

    # Installations
    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_put_installation",
            side_effect=AirzoneCloudError,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.house",
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.house")
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 23.0

    # Zones
    with (
        patch(
            "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
            side_effect=AirzoneCloudError,
        ),
        pytest.raises(__HAC_KEEP__Error),
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {
                ATTR_ENTITY_ID: "climate.salon",
                ATTR_TEMPERATURE: 20.5,
            },
            blocking=True,
        )

    state = hass.states.get("climate.salon")
    assert state.attributes[ClimateEntityStateAttribute.TARGET_TEMPERATURE] == 24.0
