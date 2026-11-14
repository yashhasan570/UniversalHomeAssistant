"""Tests for the Slide Local switch platform."""

from unittest.mock import AsyncMock

from goslideapi.goslideapi import (
    AuthenticationFailed,
    ClientConnectionError,
    ClientTimeoutError,
    DigestAuthCalcError,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from universalassistant.const import ATTR_ENTITY_ID, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_platform


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    await setup_platform(hass, mock_config_entry, [Platform.SWITCH])

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize(
    ("service"),
    [
        SERVICE_TURN_OFF,
        SERVICE_TURN_ON,
        SERVICE_TOGGLE,
    ],
)
async def test_services(
    hass: __HAC_KEEP__,
    service: str,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test switch."""
    await setup_platform(hass, mock_config_entry, [Platform.SWITCH])

    await hass.services.async_call(
        SWITCH_DOMAIN,
        service,
        {
            ATTR_ENTITY_ID: "switch.slide_bedroom_touchgo",
        },
        blocking=True,
    )
    mock_slide_api.slide_set_touchgo.assert_called_once()


@pytest.mark.parametrize(
    ("exception", "service"),
    [
        (ClientConnectionError, SERVICE_TURN_OFF),
        (ClientTimeoutError, SERVICE_TURN_ON),
        (AuthenticationFailed, SERVICE_TURN_OFF),
        (DigestAuthCalcError, SERVICE_TURN_ON),
    ],
)
async def test_service_exception(
    hass: __HAC_KEEP__,
    exception: Exception,
    service: str,
    mock_slide_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing button."""
    await setup_platform(hass, mock_config_entry, [Platform.SWITCH])

    mock_slide_api.slide_set_touchgo.side_effect = exception

    with pytest.raises(
        __HAC_KEEP__Error,
        match=(
            "Error while sending the request setting Touch&Go"
            f" to {service[5:]} to the device"
        ),
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            service,
            {
                ATTR_ENTITY_ID: "switch.slide_bedroom_touchgo",
            },
            blocking=True,
        )
