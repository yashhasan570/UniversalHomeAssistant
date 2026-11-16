"""Test NextDNS system health."""

import asyncio

from aiohttp import ClientError
from nextdns.const import API_ENDPOINT
from pytest_universalassistant.common import get_system_health_info
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.nextdns.const import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_nextdns_system_health(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test NextDNS system health."""
    aioclient_mock.get(API_ENDPOINT, text="")
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": "ok"}


async def test_nextdns_system_health_fail(
    hass: UniversalAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test NextDNS system health."""
    aioclient_mock.get(API_ENDPOINT, exc=ClientError)
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": {"type": "failed", "error": "unreachable"}}
