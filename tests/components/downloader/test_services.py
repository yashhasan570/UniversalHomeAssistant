"""Test downloader services."""

import asyncio
from contextlib import AbstractContextManager, nullcontext as does_not_raise

import probatio
import pytest
import requests
from requests_mock import Mocker

from universalassistant.components.downloader.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.setup import async_setup_component


@pytest.mark.usefixtures("setup_integration")
@pytest.mark.parametrize(
    ("subdir", "expected_result"),
    [
        ("test", does_not_raise()),
        ("test/path", does_not_raise()),
        ("~test/path", pytest.raises(ServiceValidationError)),
        ("~/../test/path", pytest.raises(ServiceValidationError)),
        ("../test/path", pytest.raises(ServiceValidationError)),
        (".../test/path", pytest.raises(ServiceValidationError)),
        ("/test/path", pytest.raises(ServiceValidationError)),
    ],
)
async def test_download_invalid_subdir(
    hass: __HAC_KEEP__,
    download_completed: asyncio.Event,
    download_failed: asyncio.Event,
    download_url: str,
    subdir: str,
    expected_result: AbstractContextManager,
) -> None:
    """Test service invalid subdirectory."""

    async def call_service() -> None:
        """Call the download service."""
        completed = hass.async_create_task(download_completed.wait())
        failed = hass.async_create_task(download_failed.wait())
        await hass.services.async_call(
            DOMAIN,
            "download_file",
            {
                "url": download_url,
                "subdir": subdir,
                "filename": "file.txt",
                "overwrite": True,
            },
            blocking=True,
        )
        await asyncio.wait((completed, failed), return_when=asyncio.FIRST_COMPLETED)

    with expected_result:
        await call_service()


@pytest.mark.usefixtures("setup_integration")
async def test_download_headers_passed_through(
    hass: __HAC_KEEP__,
    requests_mock: Mocker,
    download_completed: asyncio.Event,
    download_url: str,
) -> None:
    """Test that custom headers are passed to the HTTP request."""
    await hass.services.async_call(
        DOMAIN,
        "download_file",
        {
            "url": download_url,
            "headers": {"Authorization": "Bearer token123", "X-Custom": "value"},
        },
        blocking=True,
    )
    await download_completed.wait()

    assert requests_mock.last_request.headers["Authorization"] == "Bearer token123"
    assert requests_mock.last_request.headers["X-Custom"] == "value"


@pytest.mark.usefixtures("setup_integration")
@pytest.mark.parametrize(
    ("headers", "expected_result"),
    [
        (1, pytest.raises(probatio.error.Invalid)),  # Not a dictionary
        ({"Accept": "application/json"}, does_not_raise()),
        ({123: 456.789}, does_not_raise()),  # Convert numbers to strings
        (
            {"Accept": ["application/json"]},
            pytest.raises(probatio.error.MultipleInvalid),
        ),  # Value is not a string
        ({1: None}, pytest.raises(probatio.error.MultipleInvalid)),  # Value is None
        (
            {None: "application/json"},
            pytest.raises(probatio.error.MultipleInvalid),
        ),  # Key is None
    ],
)
async def test_download_headers_schema(
    hass: __HAC_KEEP__,
    download_completed: asyncio.Event,
    download_failed: asyncio.Event,
    download_url: str,
    headers: dict[str, str],
    expected_result: AbstractContextManager,
) -> None:
    """Test service with headers."""

    async def call_service() -> None:
        """Call the download service."""
        completed = hass.async_create_task(download_completed.wait())
        failed = hass.async_create_task(download_failed.wait())
        await hass.services.async_call(
            DOMAIN,
            "download_file",
            {
                "url": download_url,
                "headers": headers,
                "subdir": "test",
                "filename": "file.txt",
                "overwrite": True,
            },
            blocking=True,
        )
        await asyncio.wait((completed, failed), return_when=asyncio.FIRST_COMPLETED)

    with expected_result:
        await call_service()


@pytest.mark.usefixtures("setup_integration")
@pytest.mark.parametrize(
    ("exception", "expected_error"),
    [
        pytest.param(
            requests.exceptions.ConnectionError,
            __HAC_KEEP__Error,
            id="connection_error",
        ),
        pytest.param(
            ValueError,
            ServiceValidationError,
            id="value_error",
        ),
    ],
)
async def test_download_exceptions(
    hass: __HAC_KEEP__,
    requests_mock: Mocker,
    download_url: str,
    download_failed: asyncio.Event,
    exception: type[Exception],
    expected_error: type[Exception],
) -> None:
    """Test that exceptions during download propagate to the caller."""
    requests_mock.get(download_url, exc=exception)
    with pytest.raises(expected_error):
        await hass.services.async_call(
            DOMAIN, "download_file", {"url": download_url}, blocking=True
        )
    await download_failed.wait()


async def test_download_not_loaded(hass: __HAC_KEEP__) -> None:
    """Test the action raises when no config entry is loaded."""
    assert await async_setup_component(hass, DOMAIN, {})

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "download_file",
            {"url": "http://example.com/file.txt"},
            blocking=True,
        )
