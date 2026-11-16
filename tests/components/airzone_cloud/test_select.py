"""The select tests for the Airzone Cloud platform."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ServiceValidationError
from universalassistant.helpers import entity_registry as er

from .util import async_init_integration


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("universalassistant.components.airzone_cloud.PLATFORMS", [Platform.SELECT]):
        yield


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_airzone_create_selects(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test creation of selects."""

    config_entry = await async_init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)

    # Mode selects are only created for master zones
    assert hass.states.get("select.dormitorio_mode") is None


async def test_airzone_select_air_quality_mode(hass: UniversalAssistant) -> None:
    """Test select Air Quality mode."""

    await async_init_integration(hass)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.dormitorio_air_quality_mode",
                SelectServiceArgument.OPTION: "Invalid",
            },
            blocking=True,
        )

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.dormitorio_air_quality_mode",
                SelectServiceArgument.OPTION: "off",
            },
            blocking=True,
        )

    state = hass.states.get("select.dormitorio_air_quality_mode")
    assert state.state == "off"


async def test_airzone_select_mode(hass: UniversalAssistant) -> None:
    """Test select HVAC mode."""

    await async_init_integration(hass)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.salon_mode",
                SelectServiceArgument.OPTION: "Invalid",
            },
            blocking=True,
        )

    with patch(
        "universalassistant.components.airzone_cloud.AirzoneCloudApi.api_patch_device",
        return_value=None,
    ):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.salon_mode",
                SelectServiceArgument.OPTION: "heat",
            },
            blocking=True,
        )

    state = hass.states.get("select.salon_mode")
    assert state.state == "heat"
