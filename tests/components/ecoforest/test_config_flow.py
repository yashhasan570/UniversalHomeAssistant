"""Test the Ecoforest config flow."""

from unittest.mock import AsyncMock, patch

from pyecoforest.exceptions import EcoforestAuthenticationRequired
import pytest

from universalassistant import config_entries
from universalassistant.components.ecoforest.const import DOMAIN
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_form(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock, mock_device, config
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "pyecoforest.api.EcoforestApi.get",
        return_value=mock_device,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            config,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert "result" in result
    assert result["result"].unique_id == "1234"
    assert result["title"] == "Ecoforest 1234"
    assert result["data"] == {
        CONF_HOST: "1.1.1.1",
        CONF_USERNAME: "test-username",
        CONF_PASSWORD: "test-password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_device_already_configured(
    hass: __HAC_KEEP__, config_entry, mock_device, config
) -> None:
    """Test device already exists."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "pyecoforest.api.EcoforestApi.get",
        return_value=mock_device,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            config,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (
            EcoforestAuthenticationRequired("401"),
            "invalid_auth",
        ),
        (
            Exception("Something wrong"),
            "cannot_connect",
        ),
    ],
)
async def test_flow_fails(
    hass: __HAC_KEEP__, error: Exception, message: str, mock_device, config
) -> None:
    """Test we handle failed flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "pyecoforest.api.EcoforestApi.get",
        side_effect=error,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            config,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": message}

    with patch(
        "pyecoforest.api.EcoforestApi.get",
        return_value=mock_device,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            config,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
