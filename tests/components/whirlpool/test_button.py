"""Test the Whirlpool button platform."""

import pytest
from syrupy.assertion import SnapshotAssertion
import whirlpool

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import init_integration, snapshot_whirlpool_entities


@pytest.fixture(
    params=[
        (
            "button.single_cavity_oven_stop",
            "mock_oven_single_cavity_api",
            whirlpool.oven.Cavity.Upper,
        ),
        (
            "button.dual_cavity_oven_upper_oven_stop",
            "mock_oven_dual_cavity_api",
            whirlpool.oven.Cavity.Upper,
        ),
        (
            "button.dual_cavity_oven_lower_oven_stop",
            "mock_oven_dual_cavity_api",
            whirlpool.oven.Cavity.Lower,
        ),
    ]
)
def oven_button_entity(
    request: pytest.FixtureRequest,
) -> tuple[str, str, whirlpool.oven.Cavity]:
    """Parametrize the oven stop button entities."""
    return request.param


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: __HAC_KEEP__, snapshot: SnapshotAssertion, entity_registry: er.EntityRegistry
) -> None:
    """Test all entities."""
    await init_integration(hass)
    snapshot_whirlpool_entities(hass, entity_registry, snapshot, Platform.BUTTON)


async def test_stop_button_press(
    hass: __HAC_KEEP__,
    oven_button_entity: tuple[str, str, whirlpool.oven.Cavity],
    request: pytest.FixtureRequest,
) -> None:
    """Test pressing the stop button cancels the cook."""
    entity_id, mock_fixture, cavity = oven_button_entity
    mock = request.getfixturevalue(mock_fixture)
    await init_integration(hass)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    mock.stop_cook.assert_called_once_with(cavity)


async def test_stop_button_failure(
    hass: __HAC_KEEP__,
    oven_button_entity: tuple[str, str, whirlpool.oven.Cavity],
    request: pytest.FixtureRequest,
) -> None:
    """Test a failed stop request raises __HAC_KEEP__Error."""
    entity_id, mock_fixture, _ = oven_button_entity
    mock = request.getfixturevalue(mock_fixture)
    mock.stop_cook.return_value = False
    await init_integration(hass)

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {CommonServiceArgument.ENTITY_ID: entity_id},
            blocking=True,
        )
