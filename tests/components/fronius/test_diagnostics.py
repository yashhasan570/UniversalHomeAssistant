"""Tests for the diagnostics data provided by the Fronius integration."""

from fronius_modbus.testing import MpptModuleSpec, build_sunspec_map
from modbus_connection.mock import MockModbusConnection
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import __HAC_KEEP__

from . import mock_responses, setup_fronius_integration


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    aioclient_mock: AiohttpClientMocker,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    mock_responses(aioclient_mock)
    entry = await setup_fronius_integration(hass)

    assert await get_diagnostics_for_config_entry(
        hass,
        hass_client,
        entry,
    ) == snapshot(exclude=props("created_at", "modified_at"))


async def test_diagnostics_modbus(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    aioclient_mock: AiohttpClientMocker,
    mock_fronius_modbus: MockModbusConnection,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics with Modbus enabled."""
    mock_fronius_modbus.for_unit(1).holding.update(
        build_sunspec_map(
            [
                MpptModuleSpec(
                    id_str="String 1",
                    current=82,
                    voltage=4021,
                    power=3300,
                    energy=1_000_000,
                ),
            ]
        )
    )
    mock_responses(aioclient_mock, fixture_set="gen24")
    entry = await setup_fronius_integration(hass, is_logger=False)

    assert await get_diagnostics_for_config_entry(
        hass,
        hass_client,
        entry,
    ) == snapshot(exclude=props("created_at", "modified_at"))
