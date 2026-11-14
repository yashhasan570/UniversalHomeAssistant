"""Test RainMachine sensors."""

import logging
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.rainmachine.const import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr, entity_registry as er
from universalassistant.setup import async_setup_component


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    config: dict[str, Any],
    config_entry: MockConfigEntry,
    client: AsyncMock,
) -> None:
    """Test sensors."""
    with (
        patch("universalassistant.components.rainmachine.Client", return_value=client),
        patch("universalassistant.components.rainmachine.PLATFORMS", [Platform.SENSOR]),
    ):
        assert await async_setup_component(hass, DOMAIN, config)
        await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


async def test_device_info_hw_version_is_string(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    config: dict[str, Any],
    config_entry: MockConfigEntry,
    client: AsyncMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that hw_version is a string even when API returns int."""
    with (
        caplog.at_level(logging.WARNING, logger="universalassistant.helpers.frame"),
        patch("universalassistant.components.rainmachine.Client", return_value=client),
        patch("universalassistant.components.rainmachine.PLATFORMS", [Platform.SENSOR]),
    ):
        assert await async_setup_component(hass, DOMAIN, config)
        await hass.async_block_till_done()

    device_entry = device_registry.async_get_device_by_connection(
        (dr.CONNECTION_NETWORK_MAC, "aa:bb:cc:dd:ee:ff"), config_entry.entry_id
    )
    assert device_entry
    assert device_entry.hw_version == "3"
    assert "non-string value" not in caplog.text
