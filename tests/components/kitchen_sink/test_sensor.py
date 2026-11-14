"""The tests for the kitchen_sink sensor platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant import config_entries
from universalassistant.components.kitchen_sink import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr, entity_registry as er
from universalassistant.setup import async_setup_component


@pytest.fixture
async def sensor_only() -> None:
    """Enable only the sensor platform."""
    with patch(
        "universalassistant.components.kitchen_sink.COMPONENTS_WITH_DEMO_PLATFORM",
        [Platform.SENSOR],
    ):
        yield


@pytest.fixture
async def setup_comp(hass: __HAC_KEEP__, sensor_only):
    """Set up demo component."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()


@pytest.mark.usefixtures("setup_comp")
async def test_states(hass: __HAC_KEEP__, snapshot: SnapshotAssertion) -> None:
    """Test the expected sensor entities are added."""
    states = hass.states.async_all()
    assert set(states) == snapshot


@pytest.mark.usefixtures("setup_comp")
async def test_outlet_power_sensors_on_child_devices(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the outlet power sensors are placed on child devices of the power strip."""
    for entity_id in (
        "sensor.power_strip_with_2_sockets_outlet_1_power",
        "sensor.power_strip_with_2_sockets_outlet_2_power",
    ):
        entity_entry = entity_registry.async_get(entity_id)
        assert entity_entry is not None
        child_device = device_registry.async_get(entity_entry.device_id)
        assert isinstance(child_device, dr.ChildDeviceEntry)
        parent_device = device_registry.async_get(child_device.parent_device_id)
        assert parent_device is not None
        assert not isinstance(parent_device, dr.ChildDeviceEntry)
        assert parent_device.identifiers == {(DOMAIN, "2_ch_power_strip")}


@pytest.mark.usefixtures("sensor_only")
async def test_states_with_subentry(
    hass: __HAC_KEEP__, snapshot: SnapshotAssertion
) -> None:
    """Test the expected sensor entities are added."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        subentries_data=[
            config_entries.ConfigSubentryData(
                data={"state": 15},
                subentry_id="blabla",
                subentry_type="entity",
                title="Sensor test",
                unique_id=None,
            )
        ],
    )
    config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    states = hass.states.async_all()
    assert set(states) == snapshot
