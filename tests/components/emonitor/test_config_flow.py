"""Test the SiteSage Emonitor config flow."""

from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from aioemonitor.monitor import EmonitorNetwork, EmonitorStatus
import aiohttp
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.emonitor.const import DOMAIN
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.service_info.dhcp import DhcpServiceInfo

DHCP_SERVICE_INFO = DhcpServiceInfo(
    hostname="emonitor",
    ip="1.2.3.4",
    macaddress="aabbccddeeff",
)


def _mock_emonitor():
    return EmonitorStatus(
        MagicMock(), EmonitorNetwork("AABBCCDDEEFF", "1.2.3.4"), MagicMock()
    )


@contextmanager
def _patch_success() -> Generator[None]:
    """Patch the Emonitor status call and entry setup."""
    with (
        patch(
            "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
            return_value=_mock_emonitor(),
        ),
        patch("universalassistant.components.emonitor.async_setup_entry", return_value=None),
    ):
        yield


async def test_form(hass: UniversalAssistant) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
            return_value=_mock_emonitor(),
        ),
        patch(
            "universalassistant.components.emonitor.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.2.3.4",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Emonitor DDEEFF"
    assert result2["data"] == {
        "host": "1.2.3.4",
    }
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_unknown_error(hass: UniversalAssistant) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.2.3.4",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    with _patch_success():
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"], {CONF_HOST: "1.2.3.4"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_cannot_connect(hass: UniversalAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
        side_effect=aiohttp.ClientError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.2.3.4",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {CONF_HOST: "cannot_connect"}

    with _patch_success():
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"], {CONF_HOST: "1.2.3.4"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_dhcp_can_confirm(hass: UniversalAssistant) -> None:
    """Test DHCP discovery flow can confirm right away."""

    with patch(
        "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
        return_value=_mock_emonitor(),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_DHCP},
            data=DHCP_SERVICE_INFO,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "confirm"
    assert result["description_placeholders"] == {
        "host": "1.2.3.4",
        "name": "Emonitor DDEEFF",
    }

    with patch(
        "universalassistant.components.emonitor.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Emonitor DDEEFF"
    assert result2["data"] == {
        "host": "1.2.3.4",
    }
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_dhcp_fails_to_connect(hass: UniversalAssistant) -> None:
    """Test DHCP discovery flow that fails to connect."""

    with patch(
        "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
        side_effect=aiohttp.ClientError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_DHCP},
            data=DHCP_SERVICE_INFO,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_dhcp_already_exists(hass: UniversalAssistant) -> None:
    """Test DHCP discovery flow that fails to connect."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "1.2.3.4"},
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
        return_value=_mock_emonitor(),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_DHCP},
            data=DHCP_SERVICE_INFO,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_user_unique_id_already_exists(hass: UniversalAssistant) -> None:
    """Test creating an entry where the unique_id already exists."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "1.2.3.4"},
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "universalassistant.components.emonitor.config_flow.Emonitor.async_get_status",
            return_value=_mock_emonitor(),
        ),
        patch(
            "universalassistant.components.emonitor.async_setup_entry",
            return_value=None,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.2.3.4",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"
