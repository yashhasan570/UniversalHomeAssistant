"""Test the epson config flow."""

from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

from epson_projector.const import PWR_OFF_STATE

from universalassistant import config_entries
from universalassistant.components.epson.const import CONF_CONNECTION_TYPE, DOMAIN, HTTP
from universalassistant.const import CONF_HOST, CONF_NAME, STATE_UNAVAILABLE
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


@contextmanager
def _patch_projector_on() -> Generator[None]:
    """Patch a powered on projector and the entry setup."""
    with (
        patch("universalassistant.components.epson.Projector.get_power", return_value="01"),
        patch(
            "universalassistant.components.epson.Projector.get_serial_number",
            return_value="12345",
        ),
        patch("universalassistant.components.epson.Projector.close", return_value=True),
        patch("universalassistant.components.epson.async_setup_entry", return_value=None),
    ):
        yield


async def test_form(hass: UniversalAssistant) -> None:
    """Test we get the form."""

    with patch("universalassistant.components.epson.Projector.get_power", return_value="01"):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    assert result["step_id"] == config_entries.SOURCE_USER
    with (
        patch(
            "universalassistant.components.epson.Projector.get_power",
            return_value="01",
        ),
        patch(
            "universalassistant.components.epson.Projector.get_serial_number",
            return_value="12345",
        ),
        patch(
            "universalassistant.components.epson.async_setup_entry",
            return_value=None,
        ),
        patch(
            "universalassistant.components.epson.Projector.close",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "1.1.1.1", CONF_NAME: "test-epson"},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "test-epson"
    assert result2["data"] == {CONF_CONNECTION_TYPE: HTTP, CONF_HOST: "1.1.1.1"}
    assert result2["result"].unique_id == "12345"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: UniversalAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.epson.Projector.get_power",
        return_value=STATE_UNAVAILABLE,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "1.1.1.1", CONF_NAME: "test-epson"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    with _patch_projector_on():
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "1.1.1.1", CONF_NAME: "test-epson"},
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_powered_off(hass: UniversalAssistant) -> None:
    """Test we handle powered off during initial configuration."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.epson.Projector.get_power",
        return_value=PWR_OFF_STATE,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "1.1.1.1", CONF_NAME: "test-epson"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "powered_off"}

    with _patch_projector_on():
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "1.1.1.1", CONF_NAME: "test-epson"},
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
