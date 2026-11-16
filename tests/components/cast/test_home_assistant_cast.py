"""Test Universal Home Assistant Cast."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, async_mock_signal

from universalassistant.components.cast import DOMAIN, CastRuntimeData, universal_assistant_cast
from universalassistant.components.cast.const import SIGNAL_HASS_CAST_SHOW_VIEW
from universalassistant.components.cast.services import async_setup_services
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.core_config import async_process_ha_core_config
from universalassistant.exceptions import UniversalAssistantError, ServiceValidationError


async def _async_setup_ha_cast(hass: UniversalAssistant) -> None:
    """Set up Universal Home Assistant Cast on a loaded config entry."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    entry.runtime_data = CastRuntimeData(
        cast_platforms=MagicMock(),
        refresh_token=await universal_assistant_cast.async_setup_ha_cast(hass, entry),
    )
    entry.mock_state(hass, ConfigEntryState.LOADED)
    async_setup_services(hass)


@pytest.mark.usefixtures("mock_zeroconf")
async def test_service_show_view(hass: UniversalAssistant) -> None:
    """Test showing a view."""
    await _async_setup_ha_cast(hass)
    calls = async_mock_signal(hass, SIGNAL_HASS_CAST_SHOW_VIEW)

    # No valid URL
    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            DOMAIN,
            "show_lovelace_view",
            {"entity_id": "media_player.kitchen", "view_path": "mock_path"},
            blocking=True,
        )

    # Set valid URL
    await async_process_ha_core_config(
        hass,
        {"external_url": "https://example.com"},
    )
    await hass.services.async_call(
        DOMAIN,
        "show_lovelace_view",
        {"entity_id": "media_player.kitchen", "view_path": "mock_path"},
        blocking=True,
    )

    assert len(calls) == 1
    controller_data, entity_id, view_path, url_path = calls[0]
    assert controller_data["hass_url"] == "https://example.com"
    assert controller_data["client_id"] is None
    # Verify user did not accidentally submit their dev app id
    assert "supporting_app_id" not in controller_data
    assert entity_id == "media_player.kitchen"
    assert view_path == "mock_path"
    assert url_path is None


@pytest.mark.usefixtures("mock_zeroconf")
async def test_service_show_view_dashboard(hass: UniversalAssistant) -> None:
    """Test casting a specific dashboard."""
    await async_process_ha_core_config(
        hass,
        {"external_url": "https://example.com"},
    )
    await _async_setup_ha_cast(hass)
    calls = async_mock_signal(hass, SIGNAL_HASS_CAST_SHOW_VIEW)

    await hass.services.async_call(
        DOMAIN,
        "show_lovelace_view",
        {
            "entity_id": "media_player.kitchen",
            "view_path": "mock_path",
            "dashboard_path": "mock-dashboard",
        },
        blocking=True,
    )

    assert len(calls) == 1
    _controller_data, entity_id, view_path, url_path = calls[0]
    assert entity_id == "media_player.kitchen"
    assert view_path == "mock_path"
    assert url_path == "mock-dashboard"


@pytest.mark.usefixtures("mock_zeroconf")
async def test_use_cloud_url(hass: UniversalAssistant) -> None:
    """Test that we fall back to cloud url."""
    await async_process_ha_core_config(
        hass,
        {"internal_url": "http://example.local:8123"},
    )
    hass.config.components.add("cloud")

    await _async_setup_ha_cast(hass)
    calls = async_mock_signal(hass, SIGNAL_HASS_CAST_SHOW_VIEW)

    with patch(
        "universalassistant.components.cloud.async_remote_ui_urls",
        return_value=["https://something.nabu.casa"],
    ):
        await hass.services.async_call(
            DOMAIN,
            "show_lovelace_view",
            {"entity_id": "media_player.kitchen", "view_path": "mock_path"},
            blocking=True,
        )

    assert len(calls) == 1
    controller_data = calls[0][0]
    assert controller_data["hass_url"] == "https://something.nabu.casa"


@pytest.mark.usefixtures("mock_zeroconf")
async def test_remove_entry(hass: UniversalAssistant) -> None:
    """Test removing config entry removes user."""
    entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        title="Google Cast",
    )

    entry.add_to_hass(hass)

    with (
        patch("pychromecast.discovery.discover_chromecasts", return_value=(True, None)),
        patch("pychromecast.discovery.stop_discovery"),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert "cast" in hass.config.components

    user_id = entry.data.get("user_id")
    assert await hass.auth.async_get_user(user_id)

    assert await hass.config_entries.async_remove(entry.entry_id)
    assert not await hass.auth.async_get_user(user_id)


async def test_service_show_view_not_loaded(hass: UniversalAssistant) -> None:
    """Test showing a view without a loaded config entry."""
    async_setup_services(hass)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "show_lovelace_view",
            {"entity_id": "media_player.kitchen", "view_path": "mock_path"},
            blocking=True,
        )
