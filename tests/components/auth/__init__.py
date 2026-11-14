"""Tests for the auth component."""

from typing import Any

from pytest_universalassistant.common import ensure_auth_manager_loaded
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant import auth
from universalassistant.components.auth import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import Undefined
from universalassistant.setup import async_setup_component

from tests.test_util import mock_real_ip

BASE_CONFIG = [
    {
        "name": "Example",
        "type": "insecure_example",
        "users": [
            {"username": "test-user", "password": "test-pass", "name": "Test Name"}
        ],
    }
]

EMPTY_CONFIG = []


async def async_setup_auth(
    hass: __HAC_KEEP__,
    aiohttp_client: ClientSessionGenerator,
    provider_configs: list[dict[str, Any]] | Undefined = Undefined,
    module_configs: list[dict[str, Any]] | Undefined = Undefined,
    setup_api: bool = False,
    custom_ip: str | None = None,
):
    """Set up authentication and create an HTTP client."""
    hass.auth = await auth.auth_manager_from_config(
        hass,
        BASE_CONFIG if provider_configs is Undefined else provider_configs,
        EMPTY_CONFIG if module_configs is Undefined else module_configs,
    )
    ensure_auth_manager_loaded(hass.auth)
    await async_setup_component(hass, DOMAIN, {})
    if setup_api:
        await async_setup_component(hass, "api", {})
    if custom_ip:
        mock_real_ip(hass.http.app)(custom_ip)
    return await aiohttp_client(hass.http.app)
