"""Test the FAA Delays config flow."""

from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

from aiohttp import ClientConnectionError
import faadelays
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.faa_delays.const import DOMAIN
from universalassistant.const import CONF_ID
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.exceptions import __HAC_KEEP__Error


async def mock_valid_airport(self, *args, **kwargs):
    """Return a valid airport."""
    self.code = "test"


@contextmanager
def _patch_valid_airport() -> Generator[None]:
    """Patch a valid airport and the entry setup."""
    with (
        patch.object(faadelays.Airport, "update", new=mock_valid_airport),
        patch(
            "universalassistant.components.faa_delays.async_setup_entry", return_value=None
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
        patch.object(faadelays.Airport, "update", new=mock_valid_airport),
        patch(
            "universalassistant.components.faa_delays.async_setup_entry",
            return_value=None,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "test"
    assert result2["data"] == {
        "id": "test",
    }
    assert result2["result"].unique_id == "test"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_duplicate_error(hass: __HAC_KEEP__) -> None:
    """Test that we handle a duplicate configuration."""
    conf = {CONF_ID: "test"}

    MockConfigEntry(domain=DOMAIN, unique_id="test", data=conf).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=conf,
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test we handle a connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch("faadelays.Airport.update", side_effect=ClientConnectionError):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    with _patch_valid_airport():
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"id": "test"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_unexpected_exception(hass: __HAC_KEEP__) -> None:
    """Test we handle an unexpected exception."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch("faadelays.Airport.update", side_effect=__HAC_KEEP__Error):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    with _patch_valid_airport():
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"id": "test"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
