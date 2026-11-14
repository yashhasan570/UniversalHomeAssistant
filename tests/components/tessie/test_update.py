"""Test the Tessie update platform."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion
from tesla_fleet_api.exceptions import UnsupportedVehicle

from universalassistant.components.update import (
    ATTR_IN_PROGRESS,
    DOMAIN as UPDATE_DOMAIN,
    UpdateService,
)
from universalassistant.const import STATE_ON, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from .common import ERROR_UNKNOWN, assert_entities, setup_platform


async def test_updates(
    hass: __HAC_KEEP__, snapshot: SnapshotAssertion, entity_registry: er.EntityRegistry
) -> None:
    """Tests that update entity is correct."""

    entry = await setup_platform(hass, [Platform.UPDATE])

    assert_entities(hass, entry.entry_id, entity_registry, snapshot)

    entity_id = "update.test_update"

    with patch(
        "tesla_fleet_api.tessie.Vehicle.tessie_schedule_software_update"
    ) as mock_update:
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {CommonServiceArgument.ENTITY_ID: [entity_id]},
            blocking=True,
        )
        mock_update.assert_called_once()

    state = hass.states.get(entity_id)
    assert state.state == STATE_ON
    assert state.attributes.get(ATTR_IN_PROGRESS) == 1


async def test_update_error(hass: __HAC_KEEP__) -> None:
    """Test update transport errors are translated."""

    await setup_platform(hass, [Platform.UPDATE])

    with (
        patch(
            "tesla_fleet_api.tessie.Vehicle.tessie_schedule_software_update",
            side_effect=ERROR_UNKNOWN,
        ) as mock_update,
        pytest.raises(__HAC_KEEP__Error) as error,
    ):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {CommonServiceArgument.ENTITY_ID: ["update.test_update"]},
            blocking=True,
        )

    mock_update.assert_called_once()
    assert error.value.__cause__ == ERROR_UNKNOWN
    assert error.value.translation_domain == "tessie"
    assert error.value.translation_key == "cannot_connect"

    with (
        patch(
            "tesla_fleet_api.tessie.Vehicle.tessie_schedule_software_update",
            side_effect=UnsupportedVehicle(),
        ) as mock_update,
        pytest.raises(__HAC_KEEP__Error) as error,
    ):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            UpdateService.INSTALL,
            {CommonServiceArgument.ENTITY_ID: ["update.test_update"]},
            blocking=True,
        )

    mock_update.assert_called_once()
    assert isinstance(error.value.__cause__, UnsupportedVehicle)
    assert error.value.translation_domain == "tessie"
    assert error.value.translation_key == "command_failed"
