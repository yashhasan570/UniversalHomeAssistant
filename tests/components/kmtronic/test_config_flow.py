"""Test the kmtronic config flow."""

from collections.abc import Generator
from contextlib import contextmanager
from http import HTTPStatus
from unittest.mock import AsyncMock, Mock, patch

from aiohttp import ClientConnectorError, ClientResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant import config_entries
from universalassistant.components.kmtronic.const import CONF_REVERSE, DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


@contextmanager
def _patch_get_status() -> Generator[None]:
    """Patch a successful status request."""
    with patch(
        "universalassistant.components.kmtronic.config_flow.KMTronicHubAPI.async_get_status",
        return_value=[Mock()],
    ):
        yield


async def test_form(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "universalassistant.components.kmtronic.config_flow.KMTronicHubAPI.async_get_status",
        return_value=[Mock()],
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "1.1.1.1"
    assert result2["data"] == {
        "host": "1.1.1.1",
        "username": "test-username",
        "password": "test-password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_options(
    hass: __HAC_KEEP__, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test that the options form."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "host": "1.1.1.1",
            "username": "admin",
            "password": "admin",
        },
    )
    config_entry.add_to_hass(hass)

    aioclient_mock.get(
        "http://1.1.1.1/status.xml",
        text="<response><relay0>0</relay0><relay1>0</relay1></response>",
    )
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={CONF_REVERSE: True}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert config_entry.options == {CONF_REVERSE: True}

    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED


async def test_form_invalid_auth(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.kmtronic.config_flow.KMTronicHubAPI.async_get_status",
        side_effect=ClientResponseError(None, None, status=HTTPStatus.BAD_REQUEST),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}

    with _patch_get_status():
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.kmtronic.config_flow.KMTronicHubAPI.async_get_status",
        side_effect=ClientConnectorError(None, Mock()),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    with _patch_get_status():
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_unknown_error(hass: __HAC_KEEP__) -> None:
    """Test we handle unknown errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.kmtronic.config_flow.KMTronicHubAPI.async_get_status",
        side_effect=Exception(),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    with _patch_get_status():
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                "host": "1.1.1.1",
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
