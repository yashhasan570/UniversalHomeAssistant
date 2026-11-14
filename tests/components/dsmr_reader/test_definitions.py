"""Test the DSMR Reader definitions."""

import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_mqtt_message

from universalassistant.components.dsmr_reader.const import DOMAIN
from universalassistant.components.dsmr_reader.definitions import (
    dsmr_transform,
    tariff_transform,
)
from universalassistant.const import STATE_UNKNOWN
from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("20", 2.0),
        ("version 5", "version 5"),
    ],
)
async def test_dsmr_transform(input, expected) -> None:
    """Test the dsmr_transform function."""
    assert dsmr_transform(input) == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("1", "low"),
        ("0", "high"),
    ],
)
async def test_tariff_transform(input, expected) -> None:
    """Test the tariff_transform function."""
    assert tariff_transform(input) == expected


@pytest.mark.usefixtures("mqtt_mock")
async def test_entity_tariff(hass: __HAC_KEEP__) -> None:
    """Test DSMRReaderSensorEntityDescription with a tariff transform."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        title=DOMAIN,
        options={},
        entry_id="TEST_ENTRY_ID",
        unique_id="UNIQUE_TEST_ID",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Test if the payload is empty
    async_fire_mqtt_message(hass, "dsmr/meter-stats/electricity_tariff", "")
    await hass.async_block_till_done()

    electricity_tariff = "sensor.electricity_tariff"
    assert hass.states.get(electricity_tariff).state == STATE_UNKNOWN

    # Test high tariff
    async_fire_mqtt_message(hass, "dsmr/meter-stats/electricity_tariff", "0")
    await hass.async_block_till_done()
    assert hass.states.get(electricity_tariff).state == "high"

    # Test low tariff
    async_fire_mqtt_message(hass, "dsmr/meter-stats/electricity_tariff", "1")
    await hass.async_block_till_done()
    assert hass.states.get(electricity_tariff).state == "low"


@pytest.mark.usefixtures("entity_registry_enabled_by_default", "mqtt_mock")
async def test_entity_dsmr_transform(hass: __HAC_KEEP__) -> None:
    """Test DSMRReaderSensorEntityDescription state when a dsmr transform is needed."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        title=DOMAIN,
        options={},
        entry_id="TEST_ENTRY_ID",
        unique_id="UNIQUE_TEST_ID",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Test dsmr version, if it's a digit
    async_fire_mqtt_message(hass, "dsmr/meter-stats/dsmr_version", "42")
    await hass.async_block_till_done()

    dsmr_version = "sensor.dsmr_version"
    assert hass.states.get(dsmr_version).state == "4.2"

    # Test dsmr version, if it's not a digit
    async_fire_mqtt_message(hass, "dsmr/meter-stats/dsmr_version", "version 5")
    await hass.async_block_till_done()

    assert hass.states.get(dsmr_version).state == "version 5"
