"""Test the binary sensor platform of ping."""

from datetime import timedelta
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from icmplib import Host
import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.ping.const import CONF_IMPORTED_BY, DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.setup import async_setup_component


@pytest.mark.usefixtures("setup_integration")
async def test_setup_and_update(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    freezer: FrozenDateTimeFactory,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor setup and update."""

    # check if binary sensor is there
    entry = entity_registry.async_get("binary_sensor.10_10_10_10")
    assert entry == snapshot(exclude=props("unique_id"))

    state = hass.states.get("binary_sensor.10_10_10_10")
    assert state == snapshot

    # check if the sensor turns off.
    with patch(
        "universalassistant.components.ping.helpers.async_ping",
        return_value=Host(address="10.10.10.10", packets_sent=10, rtts=[]),
    ):
        freezer.tick(timedelta(minutes=6))
        await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.10_10_10_10")
    assert state == snapshot


async def test_disabled_after_import(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test if binary sensor is disabled after import."""
    config_entry.add_to_hass(hass)
    hass.config_entries.async_update_entry(
        config_entry, data={CONF_IMPORTED_BY: "device_tracker"}
    )

    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    # check if entity is disabled after import by device tracker
    entry = entity_registry.async_get("binary_sensor.10_10_10_10")
    assert entry
    assert entry.disabled
    assert entry.disabled_by is er.RegistryEntryDisabler.INTEGRATION
