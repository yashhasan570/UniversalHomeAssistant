"""Test the UPB Control config flow."""

from asyncio import TimeoutError
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from universalassistant import config_entries
from universalassistant.components.upb.const import DOMAIN
from universalassistant.config_entries import ConfigFlowResult
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


def mocked_upb(sync_complete: bool = True, config_ok: bool = True):
    """Mock UPB lib."""

    def _add_handler(_, callback):
        callback()

    def _dummy_add_handler(_, _callback):
        pass

    upb_mock = AsyncMock()
    type(upb_mock).network_id = PropertyMock(return_value="42")
    type(upb_mock).config_ok = PropertyMock(return_value=config_ok)
    type(upb_mock).disconnect = MagicMock()
    type(upb_mock).add_handler = MagicMock()
    upb_mock.add_handler.side_effect = (
        _add_handler if sync_complete else _dummy_add_handler
    )
    return patch(
        "universalassistant.components.upb.config_flow.upb_lib.UpbPim", return_value=upb_mock
    )


async def valid_flow(
    hass: UniversalAssistant,
    device: str = "socket://1.2.3.4:2101",
    sync_complete: bool = True,
    config_ok: bool = True,
) -> ConfigFlowResult:
    """Get result dict that are standard for most tests."""

    with (
        mocked_upb(sync_complete, config_ok),
        patch("universalassistant.components.upb.async_setup_entry", return_value=None),
    ):
        flow = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        return await hass.config_entries.flow.async_configure(
            flow["flow_id"],
            {"device": device, "file_path": "upb.upe"},
        )


async def test_full_upb_flow_with_serial_port(hass: UniversalAssistant) -> None:
    """Test a full UPB config flow with serial port."""

    with (
        mocked_upb(),
        patch(
            "universalassistant.components.upb.async_setup_entry", return_value=None
        ) as mock_setup_entry,
    ):
        flow = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        result = await hass.config_entries.flow.async_configure(
            flow["flow_id"],
            {
                "device": "/dev/ttyS0",
                "file_path": "upb.upe",
            },
        )
        await hass.async_block_till_done()

    assert flow["type"] is FlowResultType.FORM
    assert flow["errors"] == {}
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "UPB"
    assert result["data"] == {
        "device": "/dev/ttyS0",
        "file_path": "upb.upe",
    }
    assert result["result"].unique_id == "42"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_user_with_tcp_upb(hass: UniversalAssistant) -> None:
    """Test we can setup a TCP upb."""
    result = await valid_flow(hass, device="socket://1.2.3.4:2101")
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "device": "socket://1.2.3.4:2101",
        "file_path": "upb.upe",
    }
    assert result["result"].unique_id == "42"
    await hass.async_block_till_done()


async def test_form_cannot_connect(hass: UniversalAssistant) -> None:
    """Test we handle cannot connect error."""

    with patch(
        "universalassistant.components.upb.config_flow.asyncio.timeout",
        side_effect=TimeoutError,
    ):
        result = await valid_flow(hass, sync_complete=False)

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    with (
        mocked_upb(),
        patch("universalassistant.components.upb.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"device": "socket://1.2.3.4:2101", "file_path": "upb.upe"},
        )
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_form_missing_upb_file(hass: UniversalAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await valid_flow(hass, config_ok=False)
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_upb_file"}

    with (
        mocked_upb(),
        patch("universalassistant.components.upb.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"device": "socket://1.2.3.4:2101", "file_path": "upb.upe"},
        )
        await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_form_user_with_already_configured(hass: UniversalAssistant) -> None:
    """Test we can setup a TCP upb."""
    _ = await valid_flow(hass)
    result2 = await valid_flow(hass)
    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"
    await hass.async_block_till_done()
