"""Tests for Renault number entities."""

from collections.abc import Generator
from typing import Any
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import async_load_fixture, snapshot_platform
from renault_api.kamereon import schemas
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    ATTR_VALUE,
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
)
from universalassistant.components.renault.const import DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import ATTR_ASSUMED_STATE, ATTR_ENTITY_ID, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ServiceValidationError
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.usefixtures("patch_renault_account", "patch_get_vehicles")


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("universalassistant.components.renault.PLATFORMS", [Platform.NUMBER]):
        yield


@pytest.mark.usefixtures("fixtures_with_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_numbers(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault number entities."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_no_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_number_empty(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault number entities with empty data from Renault."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_invalid_upstream_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_number_errors(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault number entities with temporary failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_access_denied_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_number_access_denied(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault number entities with access denied failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0


@pytest.mark.usefixtures("fixtures_with_not_supported_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_number_not_supported(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault number entities with not supported failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0


@pytest.mark.usefixtures("fixtures_with_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
@pytest.mark.parametrize(
    ("service_data", "expected_min", "expected_target"),
    [
        (
            {
                ATTR_ENTITY_ID: "number.reg_zoe_40_minimum_charge_level",
                ATTR_VALUE: 20,
            },
            20,
            80,
        ),
        (
            {
                ATTR_ENTITY_ID: "number.reg_zoe_40_target_charge_level",
                ATTR_VALUE: 90,
            },
            15,
            90,
        ),
    ],
)
async def test_number_action(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    service_data: dict[str, Any],
    expected_min: int,
    expected_target: int,
) -> None:
    """Test that service invokes renault_api with correct data for min charge limit."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    min_charge_level = hass.states.get("number.reg_zoe_40_minimum_charge_level")
    target_charge_level = hass.states.get("number.reg_zoe_40_target_charge_level")
    assert min_charge_level.state == "15"
    assert target_charge_level.state == "80"
    assert not min_charge_level.attributes.get(ATTR_ASSUMED_STATE)
    assert not target_charge_level.attributes.get(ATTR_ASSUMED_STATE)

    with patch(
        "renault_api.renault_vehicle.RenaultVehicle.set_battery_soc",
        return_value=(
            schemas.KamereonVehicleBatterySocActionDataSchema.loads(
                await async_load_fixture(hass, "action.set_battery_soc.json", DOMAIN)
            )
        ),
    ) as mock_action:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            service_data=service_data,
            blocking=True,
        )
    assert len(mock_action.mock_calls) == 1
    mock_action.assert_awaited_once_with(min=expected_min, target=expected_target)

    # Verify optimistic update of coordinator data
    min_charge_level = hass.states.get("number.reg_zoe_40_minimum_charge_level")
    target_charge_level = hass.states.get("number.reg_zoe_40_target_charge_level")
    assert min_charge_level.state == str(expected_min)
    assert target_charge_level.state == str(expected_target)
    assert min_charge_level.attributes.get(ATTR_ASSUMED_STATE)
    assert target_charge_level.attributes.get(ATTR_ASSUMED_STATE)


@pytest.mark.usefixtures("fixtures_with_no_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
@pytest.mark.parametrize(
    "service_data",
    [
        {
            ATTR_ENTITY_ID: "number.reg_zoe_40_minimum_charge_level",
            ATTR_VALUE: 20,
        },
        {
            ATTR_ENTITY_ID: "number.reg_zoe_40_target_charge_level",
            ATTR_VALUE: 90,
        },
    ],
)
async def test_number_action_(
    hass: __HAC_KEEP__, config_entry: ConfigEntry, service_data: dict[str, Any]
) -> None:
    """Test that service invokes renault_api with correct data for min charge limit."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    with pytest.raises(
        ServiceValidationError,
        match="Battery state of charge data is currently unavailable",
    ):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            service_data=service_data,
            blocking=True,
        )
