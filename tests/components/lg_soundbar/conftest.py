"""Common fixtures for the lg_soundbar tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.lg_soundbar.const import DEFAULT_PORT, DOMAIN
from universalassistant.const import CONF_HOST, CONF_PORT


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="LG Soundbar",
        data={CONF_HOST: "127.0.0.1", CONF_PORT: DEFAULT_PORT},
        unique_id="uuid",
    )


@pytest.fixture
def mock_temescal() -> Generator[MagicMock]:
    """Mock the temescal library.

    Only the device constructor is mocked so that the real ``functions`` and
    ``equalisers`` lookup tables remain available to the media player.
    """
    with (
        patch(
            "universalassistant.components.lg_soundbar.media_player.temescal.temescal",
            autospec=True,
        ) as mock_temescal,
        patch(
            "universalassistant.components.lg_soundbar.test_connect",
            return_value={"name": "LG Soundbar", "uuid": "uuid"},
        ),
    ):
        yield mock_temescal
