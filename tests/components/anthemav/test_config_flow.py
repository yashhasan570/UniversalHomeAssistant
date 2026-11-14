"""Test the Anthem A/V Receivers config flow."""

from unittest.mock import AsyncMock, patch

from anthemav.device_error import DeviceError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.anthemav.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form_with_valid_connection(
    hass: __HAC_KEEP__, mock_connection_create: AsyncMock, mock_anthemav: AsyncMock
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with patch(
        "universalassistant.components.anthemav.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "port": 14999,
            },
        )

        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Anthem AV"
    assert result2["data"] == {
        "host": "1.1.1.1",
        "port": 14999,
        "mac": "00:00:00:00:00:01",
        "model": "MRX 520",
    }
    assert result2["result"].unique_id == "00:00:00:00:00:01"
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("mock_connection_create")
async def test_form_device_info_error(hass: __HAC_KEEP__) -> None:
    """Test we handle DeviceError from library."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    with patch(
        "anthemav.Connection.create",
        side_effect=DeviceError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "port": 14999,
            },
        )

        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_receive_deviceinfo"}

    with patch(
        "universalassistant.components.anthemav.async_setup_entry",
        return_value=None,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "port": 14999,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("mock_connection_create")
async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    with patch(
        "anthemav.Connection.create",
        side_effect=OSError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "port": 14999,
            },
        )

        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    with patch(
        "universalassistant.components.anthemav.async_setup_entry",
        return_value=None,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "port": 14999,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_device_already_configured(
    hass: __HAC_KEEP__,
    mock_connection_create: AsyncMock,
    mock_anthemav: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we import existing configuration."""
    config = {
        "host": "1.1.1.1",
        "port": 14999,
    }

    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=config,
    )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "already_configured"
