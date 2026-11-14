"""Fixtures for Weather platform tests."""

from collections.abc import Generator

import pytest
from pytest_universalassistant.common import mock_config_flow, mock_platform

from universalassistant.config_entries import ConfigFlow
from universalassistant.core import __HAC_KEEP__


class MockFlow(ConfigFlow):
    """Test flow."""


@pytest.fixture
def config_flow_fixture(hass: __HAC_KEEP__) -> Generator[None]:
    """Mock config flow."""
    mock_platform(hass, "test.config_flow")

    with mock_config_flow("test", MockFlow):
        yield
