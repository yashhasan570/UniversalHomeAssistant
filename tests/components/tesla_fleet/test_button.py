"""Test the Tesla Fleet button platform."""

from copy import deepcopy
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion
from tesla_fleet_api.exceptions import NotOnWhitelistFault

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import assert_entities, setup_platform
from .const import COMMAND_OK


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    normal_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Tests that the button entities are correct."""

    await setup_platform(hass, normal_config_entry, [Platform.BUTTON])
    assert_entities(hass, normal_config_entry.entry_id, entity_registry, snapshot)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: ["button.test_wake"]},
        blocking=True,
    )


@pytest.mark.parametrize(
    ("name", "func"),
    [
        ("flash_lights", "flash_lights"),
        ("honk_horn", "honk_horn"),
        ("keyless_driving", "remote_start_drive"),
        ("play_fart", "remote_boombox"),
        ("homelink", "trigger_homelink"),
    ],
)
async def test_press(
    hass: __HAC_KEEP__, normal_config_entry: MockConfigEntry, name: str, func: str
) -> None:
    """Test pressing the API buttons."""
    await setup_platform(hass, normal_config_entry, [Platform.BUTTON])

    with patch(
        f"tesla_fleet_api.tesla.VehicleFleet.{func}",
        return_value=COMMAND_OK,
    ) as command:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: [f"button.test_{name}"]},
            blocking=True,
        )
        command.assert_called_once()


async def test_homelink_no_location(
    hass: __HAC_KEEP__, normal_config_entry: MockConfigEntry
) -> None:
    """Test pressing homelink without vehicle location raises a translated error."""
    await setup_platform(hass, normal_config_entry, [Platform.BUTTON])

    coordinator = normal_config_entry.runtime_data.vehicles[0].coordinator
    coordinator.data.pop("drive_state_latitude", None)
    coordinator.data.pop("drive_state_longitude", None)

    with (
        patch("tesla_fleet_api.tesla.VehicleFleet.trigger_homelink") as command,
        pytest.raises(__HAC_KEEP__Error) as error,
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: ["button.test_homelink"]},
            blocking=True,
        )
    assert error.value.translation_key == "homelink_no_location"
    command.assert_not_called()


async def test_press_signing_error(
    hass: __HAC_KEEP__, normal_config_entry: MockConfigEntry, mock_products: AsyncMock
) -> None:
    """Test pressing a button with a signing error."""
    # Enable Signing
    new_product = deepcopy(mock_products.return_value)
    new_product["response"][0]["command_signing"] = "required"
    mock_products.return_value = new_product

    with (
        patch("universalassistant.components.tesla_fleet.TeslaFleetApi.get_private_key"),
    ):
        await setup_platform(hass, normal_config_entry, [Platform.BUTTON])

    with (
        patch("universalassistant.components.tesla_fleet.TeslaFleetApi.get_private_key"),
        patch(
            "tesla_fleet_api.tesla.VehicleSigned.flash_lights",
            side_effect=NotOnWhitelistFault,
        ),
        pytest.raises(__HAC_KEEP__Error) as error,
    ):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: ["button.test_flash_lights"]},
            blocking=True,
        )
    assert error.from_exception(NotOnWhitelistFault)
