"""Test Prusalink camera."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant.components.prusalink import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
def setup_camera_platform_only():
    """Only setup camera platform."""
    with patch("universalassistant.components.prusalink.PLATFORMS", [Platform.CAMERA]):
        yield


async def test_camera_no_job(
    hass: UniversalAssistant,
    mock_config_entry,
    mock_api,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test camera while no job active."""
    assert await async_setup_component(hass, DOMAIN, {})
    state = hass.states.get("camera.workshop_mock_title_preview")
    assert state is not None
    assert state.state == "unavailable"

    client = await hass_client()
    resp = await client.get("/api/camera_proxy/camera.workshop_mock_title_preview")
    assert resp.status == 500


async def test_camera_idle_job_mk3(
    hass: UniversalAssistant,
    mock_config_entry,
    mock_api,
    mock_job_api_idle_mk3,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test camera while job state is idle (MK3)."""
    assert await async_setup_component(hass, DOMAIN, {})
    state = hass.states.get("camera.workshop_mock_title_preview")
    assert state is not None
    assert state.state == "unavailable"

    client = await hass_client()
    resp = await client.get("/api/camera_proxy/camera.workshop_mock_title_preview")
    assert resp.status == 500


async def test_camera_active_job(
    hass: UniversalAssistant,
    mock_config_entry,
    mock_api,
    mock_job_api_printing,
    hass_client: ClientSessionGenerator,
) -> None:
    """Test camera while job active."""
    assert await async_setup_component(hass, DOMAIN, {})
    state = hass.states.get("camera.workshop_mock_title_preview")
    assert state is not None
    assert state.state == "idle"

    client = await hass_client()

    with patch("pyprusalink.PrusaLink.get_file", return_value=b"hello"):
        resp = await client.get("/api/camera_proxy/camera.workshop_mock_title_preview")
        assert resp.status == 200
        assert await resp.read() == b"hello"

    # Make sure we hit cached value.
    with patch("pyprusalink.PrusaLink.get_file", side_effect=ValueError):
        resp = await client.get("/api/camera_proxy/camera.workshop_mock_title_preview")
        assert resp.status == 200
        assert await resp.read() == b"hello"
