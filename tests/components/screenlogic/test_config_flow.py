"""Test the Pentair ScreenLogic config flow."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from screenlogicpy import ScreenLogicError
from screenlogicpy.const.common import (
    SL_GATEWAY_IP,
    SL_GATEWAY_NAME,
    SL_GATEWAY_PORT,
    SL_GATEWAY_SUBTYPE,
    SL_GATEWAY_TYPE,
)

from universalassistant import config_entries
from universalassistant.components.screenlogic.config_flow import (
    GATEWAY_MANUAL_ENTRY,
    GATEWAY_SELECT_KEY,
)
from universalassistant.components.screenlogic.const import DOMAIN
from universalassistant.const import CONF_IP_ADDRESS, CONF_PORT
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.service_info.dhcp import DhcpServiceInfo


async def test_flow_discovery(hass: __HAC_KEEP__) -> None:
    """Test the flow works with basic discovery."""

    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        return_value=[
            {
                SL_GATEWAY_IP: "1.1.1.1",
                SL_GATEWAY_PORT: 80,
                SL_GATEWAY_TYPE: 12,
                SL_GATEWAY_SUBTYPE: 2,
                SL_GATEWAY_NAME: "Pentair: 01-01-01",
            },
        ],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "gateway_select"

    with patch(
        "universalassistant.components.screenlogic.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={GATEWAY_SELECT_KEY: "00:c0:33:01:01:01"}
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Pentair: 01-01-01"
    assert result2["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
    }
    assert result2["result"].unique_id == "00:c0:33:01:01:01"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_flow_discover_none(hass: __HAC_KEEP__) -> None:
    """Test when nothing is discovered."""

    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        return_value=[],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "gateway_entry"


async def test_flow_replace_ignored(hass: __HAC_KEEP__) -> None:
    """Test we can replace ignored entries."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="00:c0:33:01:01:01",
        source=config_entries.SOURCE_IGNORE,
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        return_value=[
            {
                SL_GATEWAY_IP: "1.1.1.1",
                SL_GATEWAY_PORT: 80,
                SL_GATEWAY_TYPE: 12,
                SL_GATEWAY_SUBTYPE: 2,
                SL_GATEWAY_NAME: "Pentair: 01-01-01",
            },
        ],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "gateway_select"

    with patch(
        "universalassistant.components.screenlogic.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={GATEWAY_SELECT_KEY: "00:c0:33:01:01:01"}
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Pentair: 01-01-01"
    assert result2["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
    }
    assert result2["result"].unique_id == "00:c0:33:01:01:01"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_flow_discover_error(hass: __HAC_KEEP__) -> None:
    """Test when discovery errors."""

    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        side_effect=ScreenLogicError("Fake error"),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "gateway_entry"

    with (
        patch(
            "universalassistant.components.screenlogic.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
        patch(
            "universalassistant.components.screenlogic.config_flow.login.async_get_mac_address",
            return_value="00-C0-33-01-01-01",
        ),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Pentair: 01-01-01"
    assert result3["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_dhcp(hass: __HAC_KEEP__) -> None:
    """Test DHCP discovery flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_DHCP},
        data=DhcpServiceInfo(
            hostname="Pentair: 01-01-01",
            ip="1.1.1.1",
            macaddress="aabbccddeeff",
        ),
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "gateway_entry"

    with (
        patch(
            "universalassistant.components.screenlogic.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
        patch(
            "universalassistant.components.screenlogic.config_flow.login.async_get_mac_address",
            return_value="00-C0-33-01-01-01",
        ),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Pentair: 01-01-01"
    assert result3["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
    }
    assert result3["result"].unique_id == "00:c0:33:01:01:01"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_manual_entry(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""

    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        return_value=[
            {
                SL_GATEWAY_IP: "1.1.1.1",
                SL_GATEWAY_PORT: 80,
                SL_GATEWAY_TYPE: 12,
                SL_GATEWAY_SUBTYPE: 2,
                SL_GATEWAY_NAME: "Pentair: 01-01-01",
            },
        ],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == "gateway_select"

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={GATEWAY_SELECT_KEY: GATEWAY_MANUAL_ENTRY}
    )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {}
    assert result2["step_id"] == "gateway_entry"

    with (
        patch(
            "universalassistant.components.screenlogic.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
        patch(
            "universalassistant.components.screenlogic.config_flow.login.async_get_mac_address",
            return_value="00-C0-33-01-01-01",
        ),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Pentair: 01-01-01"
    assert result3["data"] == {
        CONF_IP_ADDRESS: "1.1.1.1",
        CONF_PORT: 80,
    }
    assert result3["result"].unique_id == "00:c0:33:01:01:01"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test we handle cannot connect error."""
    with patch(
        "universalassistant.components.screenlogic.config_flow.discovery.async_discover",
        return_value=[],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    with patch(
        "universalassistant.components.screenlogic.config_flow.login.async_get_mac_address",
        side_effect=ScreenLogicError("Failed to connect to host at 1.1.1.1:80"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {CONF_IP_ADDRESS: "cannot_connect"}

    with (
        patch(
            "universalassistant.components.screenlogic.async_setup_entry",
            return_value=None,
        ),
        patch(
            "universalassistant.components.screenlogic.config_flow.login.async_get_mac_address",
            return_value="00-C0-33-01-01-01",
        ),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.1.1.1",
                CONF_PORT: 80,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
