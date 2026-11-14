"""Fixtures for the TOLO Sauna tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from tololib import LampMode

from universalassistant.components.tolo.const import DOMAIN
from universalassistant.const import CONF_HOST


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a TOLO Sauna config entry."""
    return MockConfigEntry(domain=DOMAIN, data={CONF_HOST: "127.0.0.1"})


@pytest.fixture
def mock_tolo_client() -> Generator[MagicMock]:
    """Mock the TOLO client used by the coordinator."""
    with patch(
        "universalassistant.components.tolo.coordinator.ToloClient", autospec=True
    ) as client_class:
        client = client_class.return_value
        client.get_status.return_value = MagicMock(lamp_on=True)
        client.get_status.return_value.model.name = "SAUNA"
        client.get_settings.return_value = MagicMock(lamp_mode=LampMode.MANUAL)
        yield client
