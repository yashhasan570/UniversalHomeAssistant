"""Common fixtures for the Aquacell tests."""

from collections.abc import Generator
import time
from unittest.mock import AsyncMock, MagicMock, patch

from aioaquacell import AquacellApi, Softener
import pytest
from pytest_universalassistant.common import MockConfigEntry, load_json_array_fixture

from universalassistant.components.aquacell.const import (
    CONF_REFRESH_TOKEN_CREATION_TIME,
    DOMAIN,
)
from universalassistant.const import CONF_EMAIL

from . import TEST_CONFIG_ENTRY, TEST_CONFIG_ENTRY_WITHOUT_BRAND


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.aquacell.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_aquacell_api() -> Generator[MagicMock]:
    """Build a fixture for the Aquacell API that returns a softener."""
    with (
        patch(
            "universalassistant.components.aquacell.AquacellApi",
            autospec=True,
        ) as mock_client,
        patch(
            "universalassistant.components.aquacell.config_flow.AquacellApi",
            new=mock_client,
        ),
    ):
        mock_aquacell_api: AquacellApi = mock_client.return_value
        mock_aquacell_api.authenticate.return_value = "refresh-token"

        softeners_dict = load_json_array_fixture(
            "aquacell/get_all_softeners_one_softener.json"
        )

        softeners = [Softener.from_dict(softener) for softener in softeners_dict]
        mock_aquacell_api.get_all_softeners.return_value = softeners

        yield mock_aquacell_api


@pytest.fixture
def mock_config_entry_expired() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Aquacell",
        unique_id=TEST_CONFIG_ENTRY[CONF_EMAIL],
        data=TEST_CONFIG_ENTRY,
    )


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Aquacell",
        unique_id=TEST_CONFIG_ENTRY[CONF_EMAIL],
        data={
            **TEST_CONFIG_ENTRY,
            CONF_REFRESH_TOKEN_CREATION_TIME: time.time(),
        },
    )


@pytest.fixture
def mock_config_entry_without_brand() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Aquacell",
        unique_id=TEST_CONFIG_ENTRY[CONF_EMAIL],
        data={
            **TEST_CONFIG_ENTRY_WITHOUT_BRAND,
            CONF_REFRESH_TOKEN_CREATION_TIME: time.time(),
        },
    )
