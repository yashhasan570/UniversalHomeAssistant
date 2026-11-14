"""Test Radarr services."""

from unittest.mock import patch

from aiopyarr import ArrAuthenticationException, ArrConnectionException
import pytest
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.radarr.const import DOMAIN
from universalassistant.components.radarr.services import (
    RadarrService,
    RadarrServiceArgument,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError

from . import create_entry, setup_integration


async def test_get_queue_service(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_queue service."""
    entry = await setup_integration(hass, aioclient_mock)

    response = await hass.services.async_call(
        DOMAIN,
        RadarrService.GET_QUEUE,
        {RadarrServiceArgument.ENTRY_ID: entry.entry_id},
        blocking=True,
        return_response=True,
    )

    # Explicit assertion for specific behavior
    assert len(response["movies"]) == 2

    # Snapshot for full structure validation
    assert response == snapshot


async def test_get_movies_service(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_movies service."""
    entry = await setup_integration(hass, aioclient_mock)

    response = await hass.services.async_call(
        DOMAIN,
        RadarrService.GET_MOVIES,
        {RadarrServiceArgument.ENTRY_ID: entry.entry_id},
        blocking=True,
        return_response=True,
    )

    # Explicit assertion for specific behavior
    assert len(response["movies"]) == 2

    # Snapshot for full structure validation
    assert response == snapshot


@pytest.mark.parametrize(
    ("service", "method"),
    [
        (RadarrService.GET_QUEUE, "async_get_queue"),
        (RadarrService.GET_MOVIES, "async_get_movies"),
    ],
)
async def test_services_api_connection_error(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    service: str,
    method: str,
) -> None:
    """Test services with API connection error."""
    entry = await setup_integration(hass, aioclient_mock)

    with (
        patch(
            f"universalassistant.components.radarr.coordinator.RadarrClient.{method}",
            side_effect=ArrConnectionException(None, "Connection failed"),
        ),
        pytest.raises(__HAC_KEEP__Error, match="Failed to connect to Radarr"),
    ):
        await hass.services.async_call(
            DOMAIN,
            service,
            {RadarrServiceArgument.ENTRY_ID: entry.entry_id},
            blocking=True,
            return_response=True,
        )


@pytest.mark.parametrize(
    ("service", "method"),
    [
        (RadarrService.GET_QUEUE, "async_get_queue"),
        (RadarrService.GET_MOVIES, "async_get_movies"),
    ],
)
async def test_get_movies_service_api_auth_error(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    service: str,
    method: str,
) -> None:
    """Test services with API authentication error."""
    entry = await setup_integration(hass, aioclient_mock)

    with (
        patch(
            f"universalassistant.components.radarr.coordinator.RadarrClient.{method}",
            side_effect=ArrAuthenticationException(None, "Authentication failed"),
        ),
        pytest.raises(__HAC_KEEP__Error, match="Authentication failed for Radarr"),
    ):
        await hass.services.async_call(
            DOMAIN,
            service,
            {RadarrServiceArgument.ENTRY_ID: entry.entry_id},
            blocking=True,
            return_response=True,
        )


@pytest.mark.parametrize(
    "service",
    [RadarrService.GET_QUEUE, RadarrService.GET_MOVIES],
)
async def test_services_invalid_entry(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    service: str,
) -> None:
    """Test get_queue with invalid entry id."""
    # Set up at least one entry so the service gets registered
    await setup_integration(hass, aioclient_mock)

    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            service,
            {RadarrServiceArgument.ENTRY_ID: "invalid_id"},
            blocking=True,
            return_response=True,
        )
    assert err.value.translation_key == "service_config_entry_not_found"


@pytest.mark.parametrize(
    "service",
    [RadarrService.GET_QUEUE, RadarrService.GET_MOVIES],
)
async def test_services_entry_not_loaded(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    service: str,
) -> None:
    """Test get_queue with entry that's not loaded."""
    # First set up one entry to register the service
    await setup_integration(hass, aioclient_mock)

    # Now create a second entry that isn't loaded
    unloaded_entry = create_entry(hass)

    with pytest.raises(ServiceValidationError) as err:
        await hass.services.async_call(
            DOMAIN,
            service,
            {RadarrServiceArgument.ENTRY_ID: unloaded_entry.entry_id},
            blocking=True,
            return_response=True,
        )
    assert err.value.translation_key == "service_config_entry_not_loaded"
