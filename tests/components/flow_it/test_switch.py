"""Test AriaQ switch platform."""

from unittest.mock import AsyncMock, patch

from flow_it_api.exceptions import FlowItAuthError, FlowItCommandError, FlowItError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    SwitchService,
)
from universalassistant.const import ATTR_ENTITY_ID, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed, __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

AIR_INTAKE_ENTITY_ID = "switch.001122334455_air_intake"
AIR_EXHAUST_ENTITY_ID = "switch.001122334455_air_exhaust"


async def test_switch_setup(
    hass: __HAC_KEEP__,
    mock_ariaq: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test switch platform setup and entity registry."""
    with patch("universalassistant.components.flow_it.PLATFORMS", [Platform.SWITCH]):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "service", "expected_flow_in", "expected_flow_out"),
    [
        (AIR_INTAKE_ENTITY_ID, SERVICE_TURN_ON, True, True),
        (AIR_INTAKE_ENTITY_ID, SERVICE_TURN_OFF, False, True),
        (AIR_EXHAUST_ENTITY_ID, SERVICE_TURN_ON, True, True),
        (AIR_EXHAUST_ENTITY_ID, SERVICE_TURN_OFF, True, False),
    ],
)
async def test_switch_turn_on_off(
    hass: __HAC_KEEP__,
    mock_ariaq: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_id: str,
    service: str,
    expected_flow_in: bool,
    expected_flow_out: bool,
) -> None:
    """Test turning on and off the switches."""
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await hass.services.async_call(
        SWITCH_DOMAIN,
        service,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )
    mock_ariaq.return_value.send_command.assert_awaited_once_with(
        "2",
        flow_in=expected_flow_in,
        flow_out=expected_flow_out,
    )


@pytest.mark.parametrize(
    ("exception", "expected_exception"),
    [
        (FlowItAuthError("Auth error"), ConfigEntryAuthFailed),
        (FlowItCommandError("Command error"), __HAC_KEEP__Error),
        (FlowItError("Generic error"), __HAC_KEEP__Error),
    ],
)
async def test_switch_exceptions(
    hass: __HAC_KEEP__,
    mock_ariaq: AsyncMock,
    mock_config_entry: MockConfigEntry,
    exception: Exception,
    expected_exception: type[Exception],
) -> None:
    """Test exception handling during switch commands."""
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    mock_ariaq.return_value.send_command.side_effect = exception

    with pytest.raises(expected_exception):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: AIR_INTAKE_ENTITY_ID},
            blocking=True,
        )
