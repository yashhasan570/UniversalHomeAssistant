"""Test the MJPEG IP Camera camera platform."""

import aiohttp
import httpx2
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
import respx

from universalassistant.components.camera import async_get_image
from universalassistant.components.mjpeg.const import (
    CONF_MJPEG_URL,
    CONF_STILL_IMAGE_URL,
    DOMAIN,
)
from universalassistant.const import (
    CONF_AUTHENTICATION,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
    HTTP_DIGEST_AUTHENTICATION,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error

ENTITY_CAMERA = "camera.my_mjpeg_camera"


@pytest.mark.usefixtures("init_integration")
@pytest.mark.parametrize(
    ("exception", "translation_key"),
    [
        pytest.param(TimeoutError, "timeout_getting_image", id="timeout"),
        pytest.param(aiohttp.ClientError, "error_getting_image", id="client_error"),
    ],
)
async def test_camera_image_error(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    exception: type[Exception],
    translation_key: str,
) -> None:
    """Test that a failed still image request raises instead of returning nothing."""
    aioclient_mock.get("http://example.com/still", exc=exception)

    with pytest.raises(__HAC_KEEP__Error) as exc_info:
        await async_get_image(hass, ENTITY_CAMERA)

    assert exc_info.value.translation_domain == DOMAIN
    assert exc_info.value.translation_key == translation_key


@pytest.mark.usefixtures("init_integration")
async def test_camera_image(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test that a still image is returned."""
    aioclient_mock.get("http://example.com/still", content=b"image_bytes")

    image = await async_get_image(hass, ENTITY_CAMERA)

    assert image.content == b"image_bytes"


@pytest.fixture
def mock_digest_config_entry() -> MockConfigEntry:
    """Return a mocked config entry that uses digest authentication."""
    return MockConfigEntry(
        title="My MJPEG Camera",
        domain=DOMAIN,
        data={},
        options={
            CONF_AUTHENTICATION: HTTP_DIGEST_AUTHENTICATION,
            CONF_MJPEG_URL: "https://example.com/mjpeg",
            CONF_PASSWORD: "supersecret",
            CONF_STILL_IMAGE_URL: "http://example.com/still",
            CONF_USERNAME: "frenck",
            CONF_VERIFY_SSL: True,
        },
    )


@respx.mock
@pytest.mark.parametrize(
    ("exception", "translation_key"),
    [
        pytest.param(TimeoutError, "timeout_getting_image", id="timeout"),
        pytest.param(
            httpx2.TimeoutException, "timeout_getting_image", id="httpx_timeout"
        ),
        pytest.param(httpx2.HTTPError, "error_getting_image", id="http_error"),
    ],
)
async def test_digest_camera_image_error(
    hass: __HAC_KEEP__,
    mock_digest_config_entry: MockConfigEntry,
    exception: type[Exception],
    translation_key: str,
) -> None:
    """Test that a failed digest image request raises instead of returning nothing."""
    mock_digest_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_digest_config_entry.entry_id)
    await hass.async_block_till_done()

    respx.get("http://example.com/still").mock(side_effect=exception("boom"))
    respx.get("https://example.com/mjpeg").mock(side_effect=exception("boom"))

    with pytest.raises(__HAC_KEEP__Error) as exc_info:
        await async_get_image(hass, ENTITY_CAMERA)

    assert exc_info.value.translation_domain == DOMAIN
    assert exc_info.value.translation_key == translation_key
