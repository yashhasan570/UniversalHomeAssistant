"""Common fixtures for the SMTP tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.smtp.const import (
    CONF_ENCRYPTION,
    CONF_REPLY_TO,
    CONF_REPLY_TO_NAME,
    CONF_SENDER_NAME,
    CONF_SERVER,
    DOMAIN,
    SUBENTRY_TYPE_RECIPIENT,
)
from universalassistant.config_entries import ConfigSubentryData
from universalassistant.const import (
    CONF_PASSWORD,
    CONF_PORT,
    CONF_SENDER,
    CONF_TIMEOUT,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
)

USER_INPUT = {
    CONF_SENDER: "email@example.com",
    CONF_SENDER_NAME: "__HA_KEEP__",
    CONF_SERVER: "mail.example.com",
    CONF_PORT: 587,
    CONF_ENCRYPTION: "starttls",
    CONF_USERNAME: "test-username",
    CONF_PASSWORD: "test-password",
    CONF_VERIFY_SSL: True,
}


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.smtp.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(name="smtp")
def mock_smtp() -> Generator[MagicMock]:
    """Mock smtplib.SMTP."""

    with patch(
        "universalassistant.components.smtp.helpers.smtplib.SMTP", autospec=True
    ) as mock_client:
        client = mock_client.return_value
        client.cls = mock_client
        yield client


@pytest.fixture(name="aiosmtplib")
def mock_aiosmtplib() -> Generator[AsyncMock]:
    """Mock aiosmtplib."""

    with (
        patch(
            "universalassistant.components.smtp.config_flow.SMTP", autospec=True
        ) as mock_client,
        patch("universalassistant.components.smtp.SMTP", new=mock_client),
    ):
        client = mock_client.return_value
        client.cls = mock_client
        yield client


@pytest.fixture(name="make_msgid")
def mock_make_msgid() -> Generator[None]:
    """Mock email.utils.make_msgid."""

    with patch(
        "universalassistant.components.smtp.notify.email.utils.make_msgid",
        return_value="<177777777700.12345.12345678901234567890@mock>",
    ):
        yield


@pytest.fixture(name="randrange")
def mock_randrange() -> Generator[None]:
    """Mock random.randrange."""

    with patch(
        "random.randrange",
        side_effect=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    ):
        yield


@pytest.fixture(name="version")
def mock_version() -> Generator[None]:
    """Mock __HA_KEEP__ version."""

    with patch(
        "universalassistant.components.smtp.notify.__version__",
        "2026.10.0",
    ):
        yield


@pytest.fixture(name="client_context")
def mock_client_context() -> Generator[None]:
    """Mock client_context."""

    with (
        patch(
            "universalassistant.components.smtp.config_flow.create_client_context"
        ) as mock_client,
        patch(
            "universalassistant.components.smtp.create_client_context",
            new=mock_client,
        ),
    ):
        yield mock_client


@pytest.fixture(name="config_entry")
def mock_config_entry() -> MockConfigEntry:
    """Mock smtp configuration entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="__HA_KEEP__",
        data=USER_INPUT,
        options={
            CONF_TIMEOUT: 1312,
            CONF_REPLY_TO: "replyto@example.com",
            CONF_REPLY_TO_NAME: "Reply To Name",
        },
        entry_id="123456789",
        subentries_data=[
            ConfigSubentryData(
                data={},
                subentry_id="ABCDEF",
                subentry_type=SUBENTRY_TYPE_RECIPIENT,
                title="Recipient",
                unique_id="recipient@example.com",
            )
        ],
    )
