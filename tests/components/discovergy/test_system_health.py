"""Test Discovergy system health."""

import asyncio

from aiohttp import ClientError
from pydiscovergy.const import API_BASE
from pytest_universalassistant.common import get_system_health_info
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.discovergy.const import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.loader import async_get_integration
from universalassistant.setup import async_setup_component


async def test_discovergy_system_health(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test Discovergy system health."""
    aioclient_mock.get(API_BASE, text="")
    integration = await async_get_integration(hass, DOMAIN)
    await integration.async_get_component()
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"api_endpoint_reachable": "ok"}


async def test_discovergy_system_health_fail(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test Discovergy system health."""
    aioclient_mock.get(API_BASE, exc=ClientError)
    integration = await async_get_integration(hass, DOMAIN)
    await integration.async_get_component()
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {
        "api_endpoint_reachable": {"type": "failed", "error": "unreachable"}
    }
