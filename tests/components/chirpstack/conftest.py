"""Fixtures for the ChirpStack connection integration."""

from collections.abc import Generator
from unittest.mock import Mock, patch

from lorawan_connection.backend.chirpstack import ChirpStackConnection
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.core import UniversalAssistant


@pytest.fixture
def connection_entry(hass: UniversalAssistant) -> MockConfigEntry:
    """Create a configured connection entry."""
    entry = MockConfigEntry(
        domain="chirpstack",
        title="Home",
        unique_id="tenant",
        data={
            "endpoint": "http://server:8080",
            "api_key": "secret",
            "tenant_id": "tenant",
            "application_ids": ["application"],
        },
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture(autouse=True)
def mock_connection() -> Generator[Mock]:
    """Mock the library's transport boundary."""
    connection = Mock(spec=ChirpStackConnection)
    connection.stack_type = "chirpstack"
    connection.tenants.return_value = {"tenant": "Home"}
    connection.applications.return_value = {"application": "Sensors"}
    connection.inventory.return_value = ()
    connection.on_disconnect.return_value = Mock()
    connection.async_subscribe.return_value = Mock()
    with (
        patch(
            "universalassistant.components.chirpstack.ChirpStackConnection",
            return_value=connection,
        ),
        patch(
            "universalassistant.components.chirpstack.config_flow.ChirpStackConnection",
            return_value=connection,
        ),
    ):
        yield connection
