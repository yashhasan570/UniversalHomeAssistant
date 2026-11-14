"""Test the NO-IP component."""

from datetime import timedelta

import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components import no_ip
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component
from universalassistant.util.dt import utcnow

DOMAIN = "test.example.com"

PASSWORD = "xyz789"

UPDATE_URL = no_ip.UPDATE_URL

USERNAME = "abc@123.com"


@pytest.fixture
async def setup_no_ip(hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker) -> None:
    """Fixture that sets up NO-IP."""
    aioclient_mock.get(UPDATE_URL, params={"hostname": DOMAIN}, text="good 0.0.0.0")

    await async_setup_component(
        hass,
        no_ip.DOMAIN,
        {
            no_ip.DOMAIN: {
                "domain": DOMAIN,
                "username": USERNAME,
                "password": PASSWORD,
            }
        },
    )


async def test_setup(hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker) -> None:
    """Test setup works if update passes."""
    aioclient_mock.get(UPDATE_URL, params={"hostname": DOMAIN}, text="nochg 0.0.0.0")

    result = await async_setup_component(
        hass,
        no_ip.DOMAIN,
        {no_ip.DOMAIN: {"domain": DOMAIN, "username": USERNAME, "password": PASSWORD}},
    )
    assert result
    assert aioclient_mock.call_count == 1

    async_fire_time_changed(hass, utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    assert aioclient_mock.call_count == 2


async def test_setup_fails_if_update_fails(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test setup fails if first update fails."""
    aioclient_mock.get(UPDATE_URL, params={"hostname": DOMAIN}, text="nohost")

    result = await async_setup_component(
        hass,
        no_ip.DOMAIN,
        {no_ip.DOMAIN: {"domain": DOMAIN, "username": USERNAME, "password": PASSWORD}},
    )
    assert not result
    assert aioclient_mock.call_count == 1


async def test_setup_fails_if_wrong_auth(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test setup fails if first update fails through wrong authentication."""
    aioclient_mock.get(UPDATE_URL, params={"hostname": DOMAIN}, text="badauth")

    result = await async_setup_component(
        hass,
        no_ip.DOMAIN,
        {no_ip.DOMAIN: {"domain": DOMAIN, "username": USERNAME, "password": PASSWORD}},
    )
    assert not result
    assert aioclient_mock.call_count == 1
