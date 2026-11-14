"""Test the Renson config flow."""

from unittest.mock import patch

from universalassistant import config_entries
from universalassistant.components.renson.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with (
        patch(
            "universalassistant.components.renson.config_flow.renson",
            return_value={"title": "Renson"},
        ),
        patch(
            "universalassistant.components.renson.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Renson"
    assert result2["data"] == {
        "host": "1.1.1.1",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.renson.config_flow.renson.RensonVentilation.connect",
        return_value=False,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    with (
        patch(
            "universalassistant.components.renson.config_flow.renson",
            return_value={"title": "Renson"},
        ),
        patch(
            "universalassistant.components.renson.async_setup_entry",
            return_value=None,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY


async def test_form_unknown(hass: __HAC_KEEP__) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.renson.config_flow.renson.RensonVentilation.connect",
        side_effect=ValueError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    with (
        patch(
            "universalassistant.components.renson.config_flow.renson",
            return_value={"title": "Renson"},
        ),
        patch(
            "universalassistant.components.renson.async_setup_entry",
            return_value=None,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
