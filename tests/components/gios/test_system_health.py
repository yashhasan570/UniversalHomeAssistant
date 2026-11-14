"""Test GIOS system health."""

import asyncio

from aiohttp import ClientError
from pytest_universalassistant.common import get_system_health_info
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.gios.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.loader import async_get_integration
from universalassistant.setup import async_setup_component


async def test_gios_system_health(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test GIOS system health."""
    aioclient_mock.get("http://api.gios.gov.pl/", text="")
    integration = await async_get_integration(hass, DOMAIN)
    await integration.async_get_component()
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": "ok"}


async def test_gios_system_health_fail(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test GIOS system health."""
    aioclient_mock.get("http://api.gios.gov.pl/", exc=ClientError)
    integration = await async_get_integration(hass, DOMAIN)
    await integration.async_get_component()
    hass.config.components.add(DOMAIN)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {"can_reach_server": {"type": "failed", "error": "unreachable"}}
