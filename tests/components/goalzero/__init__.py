"""Tests for the Goal Zero Yeti integration."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, async_load_fixture
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.goalzero.const import DEFAULT_NAME, DOMAIN
from universalassistant.const import CONF_HOST, CONF_NAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.device_registry import format_mac
from universalassistant.helpers.service_info.dhcp import DhcpServiceInfo

HOST = "1.2.3.4"
MAC = "aa:bb:cc:dd:ee:ff"

CONF_DATA = {
    CONF_HOST: HOST,
    CONF_NAME: DEFAULT_NAME,
}

CONF_DHCP_FLOW = DhcpServiceInfo(
    ip=HOST,
    macaddress=format_mac("AA:BB:CC:DD:EE:FF").replace(":", ""),
    hostname="yeti",
)


def create_entry(hass: __HAC_KEEP__):
    """Add config entry in __HA_KEEP__."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONF_DATA,
        unique_id=MAC,
    )
    entry.add_to_hass(hass)
    return entry


async def create_mocked_yeti():
    """Create mocked yeti device."""
    mocked_yeti = AsyncMock()
    mocked_yeti.data = {}
    mocked_yeti.data["firmwareVersion"] = "1.0.0"
    mocked_yeti.sysdata = {}
    mocked_yeti.sysdata["model"] = "test_model"
    mocked_yeti.sysdata["macAddress"] = MAC
    return mocked_yeti


def patch_config_flow_yeti(mocked_yeti):
    """Patch Goal Zero config flow."""
    return patch(
        "universalassistant.components.goalzero.config_flow.Yeti",
        return_value=mocked_yeti,
    )


async def async_init_integration(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    skip_setup: bool = False,
) -> MockConfigEntry:
    """Set up the Goal Zero integration in __HA_KEEP__."""
    entry = create_entry(hass)
    base_url = f"http://{HOST}/"
    aioclient_mock.get(
        f"{base_url}state",
        text=await async_load_fixture(hass, "state_data.json", DOMAIN),
    )
    aioclient_mock.get(
        f"{base_url}sysinfo",
        text=await async_load_fixture(hass, "info_data.json", DOMAIN),
    )

    if not skip_setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry
