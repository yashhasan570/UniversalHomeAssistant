"""Test fixtures for mqtt component."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from random import getrandbits
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.typing import MqttMockPahoClient

from universalassistant.components import mqtt
from universalassistant.components.mqtt import DOMAIN
from universalassistant.components.mqtt.models import MessageCallbackType, ReceiveMessage
from universalassistant.components.mqtt.util import EnsureJobAfterCooldown
from universalassistant.const import EVENT_HOMEASSISTANT_STARTED
from universalassistant.core import UniversalAssistant, callback

ENTRY_DEFAULT_BIRTH_MESSAGE = {
    mqtt.CONF_BIRTH_MESSAGE: {
        mqtt.ATTR_TOPIC: "universalassistant/status",
        mqtt.ATTR_PAYLOAD: "online",
        mqtt.ATTR_QOS: 0,
        mqtt.ATTR_RETAIN: False,
    },
}


@pytest.fixture(autouse=True)
def patch_hass_config(mock_hass_config: None) -> None:
    """Patch configuration.yaml."""


@pytest.fixture
def mock_v5_protocol_check() -> bool:
    """Fixture to mock a v5 protocol test result."""
    return True


@pytest.fixture(autouse=True)
def mock_try_connection_protocol_check(
    hass: UniversalAssistant, mock_v5_protocol_check: bool
) -> Generator[MagicMock]:
    """Patch try_connection."""
    with patch(
        "universalassistant.components.mqtt.try_connection",
        return_value=mock_v5_protocol_check,
    ) as mock_try_connection:
        yield mock_try_connection


@pytest.fixture
def temp_dir_prefix() -> str:
    """Set an alternate temp dir prefix."""
    return "test"


@pytest.fixture(autouse=True)
async def mock_temp_dir(
    hass: UniversalAssistant, tmp_path: Path, temp_dir_prefix: str
) -> AsyncGenerator[str]:
    """Mock the certificate temp directory."""
    mqtt_temp_dir = f"universal-assistant-mqtt-{temp_dir_prefix}-{getrandbits(10):03x}"
    with (
        patch(
            "universalassistant.components.mqtt.util.tempfile.gettempdir",
            return_value=tmp_path,
        ),
        patch(
            # Patch temp dir name to avoid tests fail running in parallel
            "universalassistant.components.mqtt.util.TEMP_DIR_NAME",
            mqtt_temp_dir,
        ) as mocked_temp_dir,
    ):
        yield mocked_temp_dir


@pytest.fixture
def mock_debouncer(hass: UniversalAssistant) -> Generator[asyncio.Event]:
    """Mock EnsureJobAfterCooldown.

    Returns an asyncio.Event that allows to await the debouncer task to be finished.
    """
    task_done = asyncio.Event()

    class MockDeboncer(EnsureJobAfterCooldown):
        """Mock the MQTT client (un)subscribe debouncer."""

        async def _async_job(self) -> None:
            """Execute after a cooldown period."""
            await super()._async_job()
            task_done.set()

    # We mock the import of EnsureJobAfterCooldown in client.py
    with patch(
        "universalassistant.components.mqtt.client.EnsureJobAfterCooldown", MockDeboncer
    ):
        yield task_done


@pytest.fixture
async def setup_with_birth_msg_client_mock(
    hass: UniversalAssistant,
    mqtt_config_entry_data: dict[str, Any] | None,
    mqtt_config_entry_options: dict[str, Any] | None,
    mqtt_client_mock: MqttMockPahoClient,
) -> AsyncGenerator[MqttMockPahoClient]:
    """Test sending birth message."""
    birth = asyncio.Event()
    with (
        patch("universalassistant.components.mqtt.client.INITIAL_SUBSCRIBE_COOLDOWN", 0.0),
        patch("universalassistant.components.mqtt.client.DISCOVERY_COOLDOWN", 0.0),
        patch("universalassistant.components.mqtt.client.SUBSCRIBE_COOLDOWN", 0.0),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data=mqtt_config_entry_data or {mqtt.CONF_BROKER: "test-broker"},
            options=mqtt_config_entry_options or {},
            version=mqtt.CONFIG_ENTRY_VERSION,
            minor_version=mqtt.CONFIG_ENTRY_MINOR_VERSION,
        )
        entry.add_to_hass(hass)
        hass.config.components.add(DOMAIN)
        assert await hass.config_entries.async_setup(entry.entry_id)
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)

        @callback
        def wait_birth(msg: ReceiveMessage) -> None:
            """Handle birth message."""
            birth.set()

        await mqtt.async_subscribe(hass, "universalassistant/status", wait_birth)
        await hass.async_block_till_done()
        await birth.wait()
        yield mqtt_client_mock


@pytest.fixture
def recorded_calls() -> list[ReceiveMessage]:
    """Fixture to hold recorded calls."""
    return []


@pytest.fixture
def record_calls(recorded_calls: list[ReceiveMessage]) -> MessageCallbackType:
    """Fixture to record calls."""

    @callback
    def record_calls(msg: ReceiveMessage) -> None:
        """Record calls."""
        recorded_calls.append(msg)

    return record_calls


@pytest.fixture
def tag_mock() -> Generator[AsyncMock]:
    """Fixture to mock tag."""
    with patch("universalassistant.components.tag.async_scan_tag") as mock_tag:
        yield mock_tag
