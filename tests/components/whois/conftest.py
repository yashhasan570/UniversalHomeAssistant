"""Fixtures for Whois integration tests."""

from collections.abc import Generator
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.whois.const import DOMAIN
from universalassistant.const import CONF_DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="Universal Home Assistant",
        domain=DOMAIN,
        data={
            CONF_DOMAIN: "universalassistant.io",
        },
        unique_id="universalassistant.io",
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock setting up a config entry."""
    with patch(
        "universalassistant.components.whois.async_setup_entry", return_value=None
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_whois() -> Generator[MagicMock]:
    """Return a mocked query."""
    with (
        patch(
            "universalassistant.components.whois.coordinator.whoisdomain_query",
        ) as whois_mock,
        patch(
            "universalassistant.components.whois.config_flow.whoisdomain.query",
            new=whois_mock,
        ),
    ):
        domain = whois_mock.return_value
        domain.abuse_contact = "abuse@example.com"
        domain.admin = "admin@example.com"
        domain.creation_date = datetime(2019, 1, 1, 0, 0, 0)
        domain.dnssec = True
        domain.expiration_date = datetime(2023, 1, 1, 0, 0, 0)
        domain.updated_date = datetime(
            2022, 1, 1, 0, 0, 0, tzinfo=dt_util.get_time_zone("Europe/Amsterdam")
        )
        domain.name = "universalassistant.io"
        domain.name_servers = ["ns1.example.com", "ns2.example.com"]
        domain.owner = "owner@example.com"
        domain.registrant = "registrant@example.com"
        domain.registrar = "My Registrar"
        domain.reseller = "Top Domains, Low Prices"
        domain.status = "ok"
        domain.statuses = ["OK"]
        yield whois_mock


@pytest.fixture
def mock_whois_missing_some_attrs() -> Generator[Any]:
    """Return a mocked query that only sets admin."""

    class LimitedWhoisMock:
        """A limited mock of whois_query."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Mock only attributes the library always sets being available."""
            self.creation_date = datetime(2019, 1, 1, 0, 0, 0)
            self.dnssec = True
            self.expiration_date = datetime(2023, 1, 1, 0, 0, 0)
            self.updated_date = datetime(
                2022, 1, 1, 0, 0, 0, tzinfo=dt_util.get_time_zone("Europe/Amsterdam")
            )
            self.name = "universalassistant.io"
            self.name_servers = ["ns1.example.com", "ns2.example.com"]
            self.registrar = "My Registrar"
            self.status = "ok"
            self.statuses = ["OK"]

    with patch(
        "universalassistant.components.whois.coordinator.whoisdomain_query", LimitedWhoisMock
    ) as whois_mock:
        yield whois_mock


@pytest.fixture
async def init_integration(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, mock_whois: MagicMock
) -> MockConfigEntry:
    """Set up thewhois integration for testing."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return mock_config_entry


@pytest.fixture
async def init_integration_missing_some_attrs(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_whois_missing_some_attrs: MagicMock,
) -> MockConfigEntry:
    """Set up thewhois integration for testing."""
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return mock_config_entry
