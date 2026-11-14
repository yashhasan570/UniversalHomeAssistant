"""Test the Evil Genius Labs config flow."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest

from universalassistant import config_entries
from universalassistant.components.evil_genius_labs.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.util.json import JsonObjectType


@contextmanager
def _patch_device(
    all_fixture: dict[str, Any],
    info_fixture: JsonObjectType,
    product_fixture: dict[str, str],
) -> Generator[None]:
    """Patch a reachable device and the entry setup."""
    with (
        patch("pyevilgenius.EvilGeniusDevice.get_all", return_value=all_fixture),
        patch("pyevilgenius.EvilGeniusDevice.get_info", return_value=info_fixture),
        patch(
            "pyevilgenius.EvilGeniusDevice.get_product", return_value=product_fixture
        ),
        patch(
            "universalassistant.components.evil_genius_labs.async_setup_entry",
            return_value=None,
        ),
    ):
        yield


async def test_form(
    hass: __HAC_KEEP__, all_fixture, info_fixture, product_fixture
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with (
        patch(
            "pyevilgenius.EvilGeniusDevice.get_all",
            return_value=all_fixture,
        ),
        patch(
            "pyevilgenius.EvilGeniusDevice.get_info",
            return_value=info_fixture,
        ),
        patch(
            "pyevilgenius.EvilGeniusDevice.get_product",
            return_value=product_fixture,
        ),
        patch(
            "universalassistant.components.evil_genius_labs.async_setup_entry",
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
    assert result2["title"] == "Fibonacci256-23D4"
    assert result2["data"] == {
        "host": "1.1.1.1",
    }
    assert result2["result"].unique_id == "1923d4"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
    all_fixture: dict[str, Any],
    info_fixture: JsonObjectType,
    product_fixture: dict[str, str],
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "pyevilgenius.EvilGeniusDevice.get_all",
        side_effect=aiohttp.ClientError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}
    assert "Unable to connect" in caplog.text

    with _patch_device(all_fixture, info_fixture, product_fixture):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"host": "1.1.1.1"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_timeout(
    hass: __HAC_KEEP__,
    all_fixture: dict[str, Any],
    info_fixture: JsonObjectType,
    product_fixture: dict[str, str],
) -> None:
    """Test we handle timeout error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "pyevilgenius.EvilGeniusDevice.get_all",
        side_effect=TimeoutError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "timeout"}

    with _patch_device(all_fixture, info_fixture, product_fixture):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"host": "1.1.1.1"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_unknown(
    hass: __HAC_KEEP__,
    all_fixture: dict[str, Any],
    info_fixture: JsonObjectType,
    product_fixture: dict[str, str],
) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "pyevilgenius.EvilGeniusDevice.get_all",
        side_effect=ValueError("BOOM"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    with _patch_device(all_fixture, info_fixture, product_fixture):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"host": "1.1.1.1"}
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
