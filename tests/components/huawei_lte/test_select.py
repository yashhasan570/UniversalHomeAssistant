"""Tests for the Huawei LTE selects."""

from unittest.mock import MagicMock, patch

from huawei_lte_api.enums.net import LTEBandEnum, NetworkBandEnum, NetworkModeEnum
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.huawei_lte.const import DOMAIN
from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CONF_URL, CommonServiceArgument
from universalassistant.core import UniversalAssistant

from . import magic_client

SELECT_NETWORK_MODE = "select.test_router_preferred_network_mode"


async def test_set_net_mode(hass: UniversalAssistant) -> None:
    """Test setting network mode."""
    huawei_lte = MockConfigEntry(
        domain=DOMAIN, data={CONF_URL: "http://huawei-lte.example.com"}
    )
    huawei_lte.add_to_hass(hass)
    client = magic_client()
    with (
        patch("universalassistant.components.huawei_lte.Connection", MagicMock()),
        patch("universalassistant.components.huawei_lte.Client", return_value=client),
    ):
        await hass.config_entries.async_setup(huawei_lte.entry_id)
    await hass.async_block_till_done()

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: SELECT_NETWORK_MODE,
            SelectServiceArgument.OPTION: NetworkModeEnum.MODE_4G_3G_AUTO.value,
        },
        blocking=True,
    )
    await hass.async_block_till_done()
    client.net.set_net_mode.assert_called_once()
    client.net.set_net_mode.assert_called_with(
        LTEBandEnum.ALL, NetworkBandEnum.ALL, NetworkModeEnum.MODE_4G_3G_AUTO.value
    )
