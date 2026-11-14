"""Tests for the Greencell diagnostics."""

from pytest_universalassistant.common import MockConfigEntry, async_fire_mqtt_message
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__

from .conftest import (
    TEST_CURRENT_PAYLOAD_3PHASE,
    TEST_CURRENT_TOPIC,
    TEST_POWER_PAYLOAD_CHARGING,
    TEST_POWER_TOPIC,
    TEST_STATUS_PAYLOAD_CHARGING,
    TEST_STATUS_TOPIC,
    TEST_VOLTAGE_PAYLOAD_NORMAL,
    TEST_VOLTAGE_TOPIC,
)


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    setup_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    async_fire_mqtt_message(hass, TEST_CURRENT_TOPIC, TEST_CURRENT_PAYLOAD_3PHASE)
    async_fire_mqtt_message(hass, TEST_VOLTAGE_TOPIC, TEST_VOLTAGE_PAYLOAD_NORMAL)
    async_fire_mqtt_message(hass, TEST_POWER_TOPIC, TEST_POWER_PAYLOAD_CHARGING)
    async_fire_mqtt_message(hass, TEST_STATUS_TOPIC, TEST_STATUS_PAYLOAD_CHARGING)
    await hass.async_block_till_done()

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, setup_integration)
        == snapshot
    )
