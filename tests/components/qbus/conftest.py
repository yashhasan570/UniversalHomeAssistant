"""Test fixtures for qbus."""

from collections.abc import Awaitable, Callable, Generator
import json
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
    load_json_object_fixture,
)
from pytest_universalassistant.typing import MqttMockHAClient

from universalassistant.components.qbus.const import CONF_SERIAL_NUMBER, DOMAIN
from universalassistant.components.qbus.entity import QbusEntity
from universalassistant.const import CONF_ID
from universalassistant.core import UniversalAssistant
from universalassistant.util.json import JsonObjectType

from .const import FIXTURE_PAYLOAD_CONFIG, TOPIC_CONFIG


@pytest.fixture
def mock_config_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Return the default mocked config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="000001",
        data={
            CONF_ID: "UL1",
            CONF_SERIAL_NUMBER: "000001",
        },
    )
    config_entry.add_to_hass(hass)
    return config_entry


@pytest.fixture
def payload_config() -> JsonObjectType:
    """Return the config topic payload."""
    return load_json_object_fixture(FIXTURE_PAYLOAD_CONFIG, DOMAIN)


@pytest.fixture
def mock_publish_state() -> Generator[AsyncMock]:
    """Return a mocked publish state call."""
    with patch.object(QbusEntity, "_async_publish_output_state") as mock:
        yield mock


@pytest.fixture
async def setup_integration(
    hass: UniversalAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_config_entry: MockConfigEntry,
    payload_config: JsonObjectType,
) -> None:
    """Set up the integration."""

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    async_fire_mqtt_message(hass, TOPIC_CONFIG, json.dumps(payload_config))
    await hass.async_block_till_done()


@pytest.fixture
async def setup_integration_deferred(
    hass: UniversalAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_config_entry: MockConfigEntry,
    payload_config: JsonObjectType,
) -> Callable[[], Awaitable]:
    """Set up the integration."""

    async def run() -> None:
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        async_fire_mqtt_message(hass, TOPIC_CONFIG, json.dumps(payload_config))
        await hass.async_block_till_done()

    return run
