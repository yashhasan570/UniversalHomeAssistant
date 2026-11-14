"""Test the Omnilogic config flow."""

from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import patch

from omnilogic import LoginException, OmniLogicException
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.omnilogic.const import DEFAULT_PH_OFFSET, DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

DATA = {"username": "test-username", "password": "test-password"}


@contextmanager
def _patch_success() -> Iterator[None]:
    """Patch a successful connection and setup."""
    with (
        patch(
            "universalassistant.components.omnilogic.config_flow.OmniLogic.connect",
            return_value=True,
        ),
        patch(
            "universalassistant.components.omnilogic.async_setup_entry",
            return_value=None,
        ),
    ):
        yield


async def test_form(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "universalassistant.components.omnilogic.config_flow.OmniLogic.connect",
            return_value=True,
        ),
        patch(
            "universalassistant.components.omnilogic.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Omnilogic"
    assert result2["data"] == DATA
    assert result2["result"].unique_id == "test-username"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_already_configured(hass: __HAC_KEEP__) -> None:
    """Test config flow when Omnilogic component is already setup."""
    MockConfigEntry(domain=DOMAIN, data=DATA).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_with_invalid_credentials(hass: __HAC_KEEP__) -> None:
    """Test with invalid credentials."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.omnilogic.OmniLogic.connect",
        side_effect=LoginException,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "invalid_auth"}

    with _patch_success():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test if invalid response or no connection returned from Hayward."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.omnilogic.OmniLogic.connect",
        side_effect=OmniLogicException,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}

    with _patch_success():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_with_unknown_error(hass: __HAC_KEEP__) -> None:
    """Test with unknown error response from Hayward."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.omnilogic.OmniLogic.connect",
        side_effect=Exception,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "unknown"}

    with _patch_success():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            DATA,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_option_flow(hass: __HAC_KEEP__) -> None:
    """Test option flow."""
    entry = MockConfigEntry(domain=DOMAIN, data=DATA)
    entry.add_to_hass(hass)

    assert not entry.options

    with patch(
        "universalassistant.components.omnilogic.async_setup_entry", return_value=None
    ):
        result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"ph_offset": DEFAULT_PH_OFFSET},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == ""
    assert result["data"]["ph_offset"] == DEFAULT_PH_OFFSET
