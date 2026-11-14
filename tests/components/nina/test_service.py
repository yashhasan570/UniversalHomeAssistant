"""Test the Nina services."""

from unittest.mock import AsyncMock

from pynina import Warning
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.nina.const import DOMAIN
from universalassistant.components.nina.services import NinaService
from universalassistant.const import ATTR_ENTITY_ID
from universalassistant.core import UniversalAssistant

from . import setup_platform, setup_single_platform


async def test_service_registration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, mock_nina_class: AsyncMock
) -> None:
    """Test the NINA services be registered."""
    await setup_single_platform(hass, mock_config_entry, None, mock_nina_class, [])

    services = hass.services.async_services_for_domain(DOMAIN)

    assert len(services) == 1
    assert NinaService.GET_DETAILS in services


async def test_service_get_details(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nina_class: AsyncMock,
    nina_warnings: list[Warning],
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get details service."""
    await setup_platform(hass, mock_config_entry, mock_nina_class, nina_warnings)

    target_entity_id = "binary_sensor.aach_warning_1"

    result = await hass.services.async_call(
        DOMAIN,
        NinaService.GET_DETAILS,
        {ATTR_ENTITY_ID: target_entity_id},
        blocking=True,
        return_response=True,
    )
    assert result == snapshot


async def test_service_get_details_no_warning(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, mock_nina_class: AsyncMock
) -> None:
    """Test the get details service when no warning is present."""
    await setup_platform(hass, mock_config_entry, mock_nina_class, [])

    target_entity_id = "binary_sensor.aach_warning_1"

    result = await hass.services.async_call(
        DOMAIN,
        NinaService.GET_DETAILS,
        {ATTR_ENTITY_ID: target_entity_id},
        blocking=True,
        return_response=True,
    )

    assert result[target_entity_id] is None
