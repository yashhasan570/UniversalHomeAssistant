"""Fixtures for the Switch as X integration tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_universalassistant(hass: __HAC_KEEP__):
    """Set up the universalassistant integration."""
    await async_setup_component(hass, "universalassistant", {})


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock setting up a config entry."""
    with patch(
        "universalassistant.components.switch_as_x.async_setup_entry", return_value=None
    ) as mock_setup:
        yield mock_setup
