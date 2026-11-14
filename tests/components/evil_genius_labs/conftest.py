"""Test helpers for Evil Genius Labs."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    load_json_array_fixture,
    load_json_object_fixture,
)

from universalassistant.components.evil_genius_labs.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component
from universalassistant.util.json import JsonObjectType


@pytest.fixture(scope="package")
def all_fixture() -> dict[str, Any]:
    """Fixture data."""
    data = load_json_array_fixture("data.json", "evil_genius_labs")
    return {item["name"]: item for item in data}


@pytest.fixture(scope="package")
def info_fixture() -> JsonObjectType:
    """Fixture info."""
    return load_json_object_fixture("info.json", "evil_genius_labs")


@pytest.fixture(scope="package")
def product_fixture() -> dict[str, str]:
    """Fixture info."""
    return {"productName": "Fibonacci256"}


@pytest.fixture
def config_entry(hass: __HAC_KEEP__) -> MockConfigEntry:
    """Evil genius labs config entry."""
    entry = MockConfigEntry(domain=DOMAIN, data={"host": "192.168.1.113"})
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
async def setup_evil_genius_labs(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    all_fixture: dict[str, Any],
    info_fixture: JsonObjectType,
    product_fixture: dict[str, str],
    platforms: list[Platform],
) -> AsyncGenerator[None]:
    """Test up Evil Genius Labs instance."""
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
            "universalassistant.components.evil_genius_labs.PLATFORMS",
            platforms,
        ),
    ):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
        yield
