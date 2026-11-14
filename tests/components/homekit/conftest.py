"""HomeKit session fixtures."""

import asyncio
from collections.abc import Generator
from contextlib import suppress
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, async_capture_events

from universalassistant.components.device_tracker.legacy import YAML_DEVICES
from universalassistant.components.homekit.accessories import HomeDriver
from universalassistant.components.homekit.const import (
    BRIDGE_NAME,
    DOMAIN,
    EVENT_HOMEKIT_CHANGED,
)
from universalassistant.components.homekit.iidmanager import AccessoryIIDStorage
from universalassistant.components.homekit.type_cameras import Camera
from universalassistant.core import Event, __HAC_KEEP__


@pytest.fixture
def iid_storage(hass: __HAC_KEEP__) -> Generator[AccessoryIIDStorage]:
    """Mock the iid storage."""
    with patch.object(AccessoryIIDStorage, "_async_schedule_save"):
        yield AccessoryIIDStorage(hass, "")


@pytest.fixture
def run_driver(
    hass: __HAC_KEEP__, iid_storage: AccessoryIIDStorage
) -> Generator[HomeDriver]:
    """Return a custom AccessoryDriver instance for HomeKit accessory init.

    This mock does not mock async_stop, so the driver will not be stopped
    """
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    event_loop = asyncio.get_event_loop()
    with (
        patch("pyhap.accessory_driver.AsyncZeroconf"),
        patch("pyhap.accessory_driver.AccessoryEncoder"),
        patch("pyhap.accessory_driver.HAPServer"),
        patch("pyhap.accessory_driver.AccessoryDriver.publish"),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.persist",
        ),
    ):
        yield HomeDriver(
            hass,
            pincode=b"123-45-678",
            entry_id=entry.entry_id,
            entry_title="mock entry",
            bridge_name=BRIDGE_NAME,
            iid_storage=iid_storage,
            address="127.0.0.1",
            loop=event_loop,
        )


@pytest.fixture
def hk_driver(
    hass: __HAC_KEEP__, iid_storage: AccessoryIIDStorage
) -> Generator[HomeDriver]:
    """Return a custom AccessoryDriver instance for HomeKit accessory init."""
    event_loop = asyncio.get_event_loop()
    with (
        patch("pyhap.accessory_driver.AsyncZeroconf"),
        patch("pyhap.accessory_driver.AccessoryEncoder"),
        patch("pyhap.accessory_driver.HAPServer.async_stop"),
        patch("pyhap.accessory_driver.HAPServer.async_start"),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.publish",
        ),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.persist",
        ),
    ):
        yield HomeDriver(
            hass,
            pincode=b"123-45-678",
            entry_id="",
            entry_title="mock entry",
            bridge_name=BRIDGE_NAME,
            iid_storage=iid_storage,
            address="127.0.0.1",
            loop=event_loop,
        )


@pytest.fixture
def mock_hap(
    hass: __HAC_KEEP__,
    iid_storage: AccessoryIIDStorage,
    mock_zeroconf: MagicMock,
) -> Generator[HomeDriver]:
    """Return a custom AccessoryDriver instance for HomeKit accessory init."""
    event_loop = asyncio.get_event_loop()
    with (
        patch("pyhap.accessory_driver.AsyncZeroconf"),
        patch("pyhap.accessory_driver.AccessoryEncoder"),
        patch("pyhap.accessory_driver.HAPServer.async_stop"),
        patch("pyhap.accessory_driver.HAPServer.async_start"),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.publish",
        ),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.async_start",
        ),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.async_stop",
        ),
        patch(
            "pyhap.accessory_driver.AccessoryDriver.persist",
        ),
    ):
        yield HomeDriver(
            hass,
            pincode=b"123-45-678",
            entry_id="",
            entry_title="mock entry",
            bridge_name=BRIDGE_NAME,
            iid_storage=iid_storage,
            address="127.0.0.1",
            loop=event_loop,
        )


@pytest.fixture
def events(hass: __HAC_KEEP__) -> list[Event]:
    """Yield caught homekit_changed events."""
    return async_capture_events(hass, EVENT_HOMEKIT_CHANGED)


@pytest.fixture
def demo_cleanup(hass: __HAC_KEEP__) -> Generator[None]:
    """Clean up device tracker demo file."""
    yield
    with suppress(FileNotFoundError):
        os.remove(hass.config.path(YAML_DEVICES))


@pytest.fixture
def recording_transport() -> Generator[tuple[AsyncMock, AsyncMock]]:
    """Patch the HDS listener, sockets are blocked in tests."""
    with (
        patch.object(Camera, "start_recording_transport") as start,
        patch.object(Camera, "stop_recording_transport") as stop,
    ):
        yield start, stop
