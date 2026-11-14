"""Test firmware update coordinator for __HA_KEEP__ Hardware."""

from unittest.mock import AsyncMock, Mock, call, patch

from freezegun.api import FrozenDateTimeFactory
from ha_silabs_firmware_client import FirmwareManifest, ManifestMissing
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed
from yarl import URL

from universalassistant.components.universalassistant_hardware.coordinator import (
    FIRMWARE_REFRESH_INTERVAL,
    FirmwareUpdateCoordinator,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.util import dt as dt_util


async def test_firmware_update_coordinator_fetching(
    hass: __HAC_KEEP__,
    caplog: pytest.LogCaptureFixture,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the firmware update coordinator loads manifests."""
    session = async_get_clientsession(hass)

    mock_config_entry = MockConfigEntry()

    manifest = FirmwareManifest(
        url=URL("https://example.org/firmware"),
        html_url=URL("https://example.org/release_notes"),
        created_at=dt_util.utcnow(),
        firmwares=(),
    )

    mock_client = Mock()
    mock_client.async_update_data = AsyncMock(side_effect=[ManifestMissing(), manifest])

    with patch(
        "universalassistant.components.universalassistant_hardware.coordinator.FirmwareUpdateClient",
        return_value=mock_client,
    ):
        coordinator = FirmwareUpdateCoordinator(
            hass, mock_config_entry, session, "https://example.org/firmware"
        )

    listener = Mock()
    coordinator.async_add_listener(listener)

    # The first update will fail
    freezer.tick(FIRMWARE_REFRESH_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert listener.mock_calls == [call()]
    assert coordinator.data is None
    assert "GitHub release assets haven't been uploaded yet" in caplog.text

    # The second will succeed
    freezer.tick(FIRMWARE_REFRESH_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert listener.mock_calls == [call(), call()]
    assert coordinator.data == manifest

    await coordinator.async_shutdown()
