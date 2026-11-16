"""Tests for the iOS init file."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import mock_component

from universalassistant.components import ios
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
def mock_load_json():
    """Mock load_json."""
    with patch("universalassistant.components.ios.load_json_object", return_value={}):
        yield


@pytest.fixture(autouse=True)
def mock_dependencies(hass: UniversalAssistant) -> None:
    """Mock dependencies loaded."""
    mock_component(hass, "zeroconf")
    mock_component(hass, "device_tracker")


async def test_creating_entry_sets_up_sensor(hass: UniversalAssistant) -> None:
    """Test setting up iOS loads the sensor component."""
    with patch(
        "universalassistant.components.ios.sensor.async_setup_entry",
        return_value=None,
    ) as mock_setup:
        assert await async_setup_component(hass, ios.DOMAIN, {ios.DOMAIN: {}})
        await hass.async_block_till_done()

    assert len(mock_setup.mock_calls) == 1


async def test_configuring_ios_creates_entry(hass: UniversalAssistant) -> None:
    """Test that specifying config will create an entry."""
    with patch(
        "universalassistant.components.ios.async_setup_entry",
        return_value=None,
    ) as mock_setup:
        await async_setup_component(hass, ios.DOMAIN, {"ios": {"push": {}}})
        await hass.async_block_till_done()

    assert len(mock_setup.mock_calls) == 1


async def test_not_configuring_ios_not_creates_entry(hass: UniversalAssistant) -> None:
    """Test that no config will not create an entry."""
    with patch(
        "universalassistant.components.ios.async_setup_entry",
        return_value=None,
    ) as mock_setup:
        await async_setup_component(hass, ios.DOMAIN, {"foo": "bar"})
        await hass.async_block_till_done()

    assert len(mock_setup.mock_calls) == 0
