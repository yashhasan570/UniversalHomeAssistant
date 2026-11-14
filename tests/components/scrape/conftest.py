"""Fixtures for the Scrape integration."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.rest.data import DEFAULT_TIMEOUT  # pylint: disable=universal-assistant-component-root-import
from universalassistant.components.rest.schema import DEFAULT_METHOD, DEFAULT_VERIFY_SSL  # pylint: disable=universal-assistant-component-root-import
from universalassistant.components.scrape.const import (
    CONF_ENCODING,
    CONF_INDEX,
    CONF_SELECT,
    DEFAULT_ENCODING,
    DOMAIN,
)
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import (
    CONF_METHOD,
    CONF_RESOURCE,
    CONF_TIMEOUT,
    CONF_VERIFY_SSL,
)
from universalassistant.core import UniversalAssistant

from . import MockRestData


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Automatically path uuid generator."""
    with patch(
        "universalassistant.components.scrape.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(name="get_resource_config")
async def get_resource_config_to_integration_load() -> dict[str, Any]:
    """Return default minimal configuration for resource.

    To override the config, tests can be marked with:
    @pytest.mark.parametrize("get_config", [{...}])
    """
    return {
        CONF_RESOURCE: "https://www.universalassistant.io",
        CONF_METHOD: DEFAULT_METHOD,
        "auth": {},
        "additional": {
            CONF_VERIFY_SSL: DEFAULT_VERIFY_SSL,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_ENCODING: DEFAULT_ENCODING,
        },
    }


@pytest.fixture(name="get_sensor_config")
async def get_sensor_config_to_integration_load() -> tuple[dict[str, Any], ...]:
    """Return default minimal configuration for sensor.

    To override the config, tests can be marked with:
    @pytest.mark.parametrize("get_config", [{...}])
    """
    return (
        {
            "data": {
                "additional": {},
                CONF_INDEX: 0,
                CONF_SELECT: ".current-version h1",
            },
            "subentry_id": "01JZN07D8D23994A49YKS649S7",
            "subentry_type": "entity",
            "title": "Current version",
            "unique_id": None,
        },
    )


@pytest.fixture(name="get_data")
async def get_data_to_integration_load() -> MockRestData:
    """Return RestData.

    To override the config, tests can be marked with:
    @pytest.mark.parametrize("get_data", [{...}])
    """
    return MockRestData("test_scrape_sensor")


@pytest.fixture(name="loaded_entry")
async def load_integration(
    hass: UniversalAssistant,
    get_resource_config: dict[str, Any],
    get_sensor_config: tuple[dict[str, Any], ...],
    get_data: MockRestData,
) -> MockConfigEntry:
    """Set up the Scrape integration in Universal Universal Home Assistant."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        options=get_resource_config,
        entry_id="01JZN04ZJ9BQXXGXDS05WS7D6P",
        subentries_data=get_sensor_config,
        version=2,
    )

    config_entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.rest.util.RestData",
        return_value=get_data,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    return config_entry
