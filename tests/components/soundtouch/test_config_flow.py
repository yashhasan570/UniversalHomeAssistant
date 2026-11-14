"""Test config flow."""

from ipaddress import ip_address
from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from requests import RequestException
import requests_mock
from requests_mock import ANY, Mocker

from universalassistant.components.soundtouch.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER, SOURCE_ZEROCONF
from universalassistant.const import CONF_HOST, CONF_SOURCE
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

from .conftest import (
    DEVICE_1_ID,
    DEVICE_1_IP,
    DEVICE_1_NAME,
    DEVICE_1_URL,
    DEVICE_2_IP,
    DEVICE_2_URL,
)


async def test_user_flow_create_entry(
    hass: UniversalAssistant, device1_requests_mock_standby: Mocker
) -> None:
    """Test the full manual user flow from start to finish."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
    )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "user"

    with patch(
        "universalassistant.components.soundtouch.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: DEVICE_1_IP,
            },
        )

    assert len(mock_setup_entry.mock_calls) == 1

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == DEVICE_1_NAME
    assert result.get("data") == {
        CONF_HOST: DEVICE_1_IP,
    }
    assert "result" in result
    assert result["result"].unique_id == DEVICE_1_ID
    assert result["result"].title == DEVICE_1_NAME


async def test_user_flow_cannot_connect(
    hass: UniversalAssistant, requests_mock: requests_mock.Mocker, device1_info: str
) -> None:
    """Test a manual user flow with an invalid host."""
    requests_mock.get(ANY, exc=RequestException())

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
        data={
            CONF_HOST: "invalid-hostname",
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    requests_mock.get(f"{DEVICE_1_URL}/info", text=device1_info)
    with patch(
        "universalassistant.components.soundtouch.async_setup_entry", return_value=None
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={CONF_HOST: DEVICE_1_IP}
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_zeroconf_flow_create_entry(
    hass: UniversalAssistant, device1_requests_mock_standby: Mocker
) -> None:
    """Test the zeroconf flow from start to finish."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_ZEROCONF},
        data=ZeroconfServiceInfo(
            ip_address=ip_address(DEVICE_1_IP),
            ip_addresses=[ip_address(DEVICE_1_IP)],
            port=8090,
            hostname="Bose-SM2-060000000001.local.",
            type="_soundtouch._tcp.local.",
            name=f"{DEVICE_1_NAME}._soundtouch._tcp.local.",
            properties={
                "DESCRIPTION": "SoundTouch",
                "MAC": DEVICE_1_ID,
                "MANUFACTURER": "Bose Corporation",
                "MODEL": "SoundTouch",
            },
        ),
    )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "zeroconf_confirm"
    assert result.get("description_placeholders") == {"name": DEVICE_1_NAME}

    with patch(
        "universalassistant.components.soundtouch.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )

    assert len(mock_setup_entry.mock_calls) == 1

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == DEVICE_1_NAME
    assert result.get("data") == {
        CONF_HOST: DEVICE_1_IP,
    }
    assert "result" in result
    assert result["result"].unique_id == DEVICE_1_ID
    assert result["result"].title == DEVICE_1_NAME


async def test_reconfigure_flow(
    hass: UniversalAssistant,
    requests_mock: requests_mock.Mocker,
    device1_config: MockConfigEntry,
    device1_info: str,
) -> None:
    """Test reconfiguring the device host."""
    device1_config.add_to_hass(hass)

    result = await device1_config.start_reconfigure_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    requests_mock.get(f"{DEVICE_2_URL}/info", text=device1_info)
    with patch(
        "universalassistant.components.soundtouch.async_setup_entry", return_value=None
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={CONF_HOST: DEVICE_2_IP}
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert device1_config.data[CONF_HOST] == DEVICE_2_IP


async def test_reconfigure_flow_cannot_connect(
    hass: UniversalAssistant,
    requests_mock: requests_mock.Mocker,
    device1_config: MockConfigEntry,
    device1_info: str,
) -> None:
    """Test reconfigure flow recovers from a connection error."""
    device1_config.add_to_hass(hass)

    result = await device1_config.start_reconfigure_flow(hass)

    requests_mock.get(ANY, exc=RequestException())
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_HOST: DEVICE_2_IP}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["errors"] == {"base": "cannot_connect"}

    requests_mock.get(f"{DEVICE_2_URL}/info", text=device1_info)
    with patch(
        "universalassistant.components.soundtouch.async_setup_entry", return_value=None
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={CONF_HOST: DEVICE_2_IP}
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert device1_config.data[CONF_HOST] == DEVICE_2_IP


async def test_reconfigure_flow_unique_id_mismatch(
    hass: UniversalAssistant,
    requests_mock: requests_mock.Mocker,
    device1_config: MockConfigEntry,
    device2_info: str,
) -> None:
    """Test reconfigure flow aborts when pointed at a different device."""
    device1_config.add_to_hass(hass)

    result = await device1_config.start_reconfigure_flow(hass)

    requests_mock.get(f"{DEVICE_2_URL}/info", text=device2_info)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_HOST: DEVICE_2_IP}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "unique_id_mismatch"
    assert device1_config.data[CONF_HOST] == DEVICE_1_IP
