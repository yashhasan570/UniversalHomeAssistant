"""Test the Teslemetry lock platform."""

from unittest.mock import AsyncMock, patch

from aiohttp import ClientConnectionError
import pytest
from syrupy.assertion import SnapshotAssertion
from tesla_fleet_api.exceptions import InvalidCommand
from teslemetry_stream.const import Signal

from universalassistant.components.lock import DOMAIN as LOCK_DOMAIN, LockService, LockState
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError
from universalassistant.helpers import entity_registry as er

from . import assert_entities, reload_platform, setup_platform
from .const import COMMAND_ERRORS, COMMAND_OK, VEHICLE_DATA_ALT


async def test_lock(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_legacy: AsyncMock,
) -> None:
    """Tests that the lock entities are correct."""

    entry = await setup_platform(hass, [Platform.LOCK])
    assert_entities(hass, entry.entry_id, entity_registry, snapshot)


async def test_lock_alt(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_vehicle_data: AsyncMock,
    mock_legacy: AsyncMock,
) -> None:
    """Tests that the lock entities are correct."""

    mock_vehicle_data.return_value = VEHICLE_DATA_ALT
    entry = await setup_platform(hass, [Platform.LOCK])
    assert_entities(hass, entry.entry_id, entity_registry, snapshot)


async def test_lock_services(
    hass: UniversalAssistant,
) -> None:
    """Tests that the lock services work."""

    await setup_platform(hass, [Platform.LOCK])

    entity_id = "lock.test_lock"

    with patch(
        "tesla_fleet_api.teslemetry.Vehicle.door_lock",
        return_value=COMMAND_OK,
    ) as call:
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.LOCK,
            {TargetKey.ENTITY_ID: entity_id},
            blocking=True,
        )
        state = hass.states.get(entity_id)
        assert state.state == LockState.LOCKED
        call.assert_called_once()

    with patch(
        "tesla_fleet_api.teslemetry.Vehicle.door_unlock",
        return_value=COMMAND_OK,
    ) as call:
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.UNLOCK,
            {TargetKey.ENTITY_ID: entity_id},
            blocking=True,
        )
        state = hass.states.get(entity_id)
        assert state.state == LockState.UNLOCKED
        call.assert_called_once()

    entity_id = "lock.test_charge_cable_lock"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.LOCK,
            {TargetKey.ENTITY_ID: entity_id},
            blocking=True,
        )

    with patch(
        "tesla_fleet_api.teslemetry.Vehicle.charge_port_door_open",
        return_value=COMMAND_OK,
    ) as call:
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.UNLOCK,
            {TargetKey.ENTITY_ID: entity_id},
            blocking=True,
        )
        state = hass.states.get(entity_id)
        assert state.state == LockState.UNLOCKED
        call.assert_called_once()


@pytest.mark.parametrize("response", COMMAND_ERRORS)
async def test_lock_command_errors(hass: UniversalAssistant, response: dict) -> None:
    """Tests that vehicle command failures raise UniversalAssistantError."""

    await setup_platform(hass, [Platform.LOCK])

    with (
        patch(
            "tesla_fleet_api.teslemetry.Vehicle.door_lock",
            return_value=response,
        ),
        pytest.raises(UniversalAssistantError),
    ):
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.LOCK,
            {TargetKey.ENTITY_ID: "lock.test_lock"},
            blocking=True,
        )


@pytest.mark.parametrize(
    ("side_effect", "translation_key"),
    [
        pytest.param(InvalidCommand, "command_exception", id="fleet_error"),
        pytest.param(
            ClientConnectionError, "command_connection_error", id="client_error"
        ),
        pytest.param(TimeoutError, "command_connection_error", id="timeout"),
    ],
)
async def test_lock_command_exception(
    hass: UniversalAssistant, side_effect: type[BaseException], translation_key: str
) -> None:
    """Tests that a command exception raises a translated UniversalAssistantError."""

    await setup_platform(hass, [Platform.LOCK])

    with (
        patch(
            "tesla_fleet_api.teslemetry.Vehicle.door_lock",
            side_effect=side_effect,
        ),
        pytest.raises(UniversalAssistantError) as exc_info,
    ):
        await hass.services.async_call(
            LOCK_DOMAIN,
            LockService.LOCK,
            {TargetKey.ENTITY_ID: "lock.test_lock"},
            blocking=True,
        )
    assert exc_info.value.translation_key == translation_key


async def test_lock_streaming(
    hass: UniversalAssistant,
    mock_vehicle_data: AsyncMock,
    mock_add_listener: AsyncMock,
) -> None:
    """Tests that the lock entities with streaming are correct."""

    entry = await setup_platform(hass, [Platform.LOCK])

    # Stream update
    mock_add_listener.send(
        {
            "vin": VEHICLE_DATA_ALT["response"]["vin"],
            "data": {
                Signal.LOCKED: True,
                Signal.CHARGE_PORT_LATCH: "ChargePortLatchEngaged",
            },
            "createdAt": "2024-10-04T10:45:17.537Z",
        }
    )
    await hass.async_block_till_done()

    await reload_platform(hass, entry, [Platform.LOCK])

    # Assert the entities restored their values with concrete assertions
    assert hass.states.get("lock.test_lock").state == LockState.LOCKED
    assert hass.states.get("lock.test_charge_cable_lock").state == LockState.LOCKED

    # Stream update
    mock_add_listener.send(
        {
            "vin": VEHICLE_DATA_ALT["response"]["vin"],
            "data": {
                Signal.LOCKED: False,
                Signal.CHARGE_PORT_LATCH: "ChargePortLatchDisengaged",
            },
            "createdAt": "2024-10-04T10:45:17.537Z",
        }
    )
    await hass.async_block_till_done()

    await reload_platform(hass, entry, [Platform.LOCK])

    # Assert the entities restored their values with concrete assertions
    assert hass.states.get("lock.test_lock").state == LockState.UNLOCKED
    assert hass.states.get("lock.test_charge_cable_lock").state == LockState.UNLOCKED
