"""The tests for http static files."""

from http import HTTPStatus
from pathlib import Path

from aiohttp.test_utils import TestClient
import pytest
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.http import DOMAIN, StaticPathConfig
from universalassistant.components.http.static import CachingStaticResource
from universalassistant.const import EVENT_HOMEASSISTANT_START
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.http import KEY_ALLOW_CONFIGURED_CORS
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
async def http(hass: UniversalAssistant) -> None:
    """Ensure http is set up."""
    assert await async_setup_component(hass, DOMAIN, {})
    hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
    await hass.async_block_till_done()


@pytest.fixture
async def mock_http_client(hass: UniversalAssistant, aiohttp_client: ClientSessionGenerator):
    """Start the Universal Universal Home Assistant HTTP component."""
    return await aiohttp_client(hass.http.app, server_kwargs={"skip_url_asserts": True})


async def test_static_resource_show_index(
    hass: UniversalAssistant, mock_http_client: TestClient, tmp_path: Path
) -> None:
    """Test static resource will return a directory index."""
    app = hass.http.app

    resource = CachingStaticResource("/", tmp_path, show_index=True)
    app.router.register_resource(resource)
    app[KEY_ALLOW_CONFIGURED_CORS](resource)

    resp = await mock_http_client.get("/")
    assert resp.status == 200
    assert resp.content_type == "text/html"


async def test_async_register_static_paths(
    hass: UniversalAssistant, hass_client: ClientSessionGenerator
) -> None:
    """Test registering multiple static paths."""
    assert await async_setup_component(hass, "frontend", {})
    path = str(Path(__file__).parent)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig("/something", path),
            StaticPathConfig("/something_else", path),
        ]
    )

    client = await hass_client()
    resp = await client.get("/something/__init__.py")
    assert resp.status == HTTPStatus.OK
    resp = await client.get("/something_else/__init__.py")
    assert resp.status == HTTPStatus.OK
