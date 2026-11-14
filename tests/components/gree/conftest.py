"""Pytest module configuration."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from .common import FakeDiscovery, build_device_mock


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.gree.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(autouse=True, name="discovery")
def discovery_fixture():
    """Patch the discovery object."""
    with patch("universalassistant.components.gree.coordinator.Discovery") as mock:
        mock.return_value = FakeDiscovery()
        yield mock


@pytest.fixture(autouse=True, name="device")
def device_fixture():
    """Patch the device search and bind."""
    with patch(
        "universalassistant.components.gree.coordinator.Device",
        return_value=build_device_mock(),
    ) as mock:
        yield mock
