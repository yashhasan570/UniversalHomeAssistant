"""Tests for the agent_dvr component."""

from pytest_universalassistant.common import MockConfigEntry, async_load_fixture
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.agent_dvr.const import DOMAIN, SERVER_URL
from universalassistant.const import CONF_HOST, CONF_PORT, CONTENT_TYPE_JSON
from universalassistant.core import UniversalAssistant

CONF_DATA = {
    CONF_HOST: "example.local",
    CONF_PORT: 8090,
    SERVER_URL: "http://example.local:8090/",
}


def create_entry(hass: UniversalAssistant):
    """Add config entry in Universal Universal Home Assistant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="c0715bba-c2d0-48ef-9e3e-bc81c9ea4447",
        data=CONF_DATA,
    )
    entry.add_to_hass(hass)
    return entry


async def init_integration(
    hass: UniversalAssistant,
    aioclient_mock: AiohttpClientMocker,
    skip_setup: bool = False,
) -> MockConfigEntry:
    """Set up the Agent DVR integration in Universal Universal Home Assistant."""

    aioclient_mock.get(
        "http://example.local:8090/command.cgi?cmd=getStatus",
        text=await async_load_fixture(hass, "status.json", DOMAIN),
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )
    aioclient_mock.get(
        "http://example.local:8090/command.cgi?cmd=getObjects",
        text=await async_load_fixture(hass, "objects.json", DOMAIN),
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )
    entry = create_entry(hass)

    if not skip_setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
