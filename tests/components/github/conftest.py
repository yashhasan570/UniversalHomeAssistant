"""conftest for the GitHub integration."""

import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

from aiogithubapi import (
    GitHubAuthenticatedUserModel,
    GitHubLoginDeviceModel,
    GitHubLoginOauthModel,
    GitHubRateLimitModel,
)
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_load_json_object_fixture,
    load_json_object_fixture,
)

from universalassistant.components.github.const import (
    CONF_REPOSITORY,
    DOMAIN,
    SUBENTRY_TYPE_REPOSITORY,
)
from universalassistant.config_entries import ConfigSubentryDataWithId
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import __HAC_KEEP__

from .const import MOCK_ACCESS_TOKEN


@pytest.fixture
def mock_subentries() -> list[ConfigSubentryDataWithId]:
    """Fixture for subentries."""
    return [
        ConfigSubentryDataWithId(
            data={
                CONF_REPOSITORY: "universal-assistant/core",
            },
            subentry_type=SUBENTRY_TYPE_REPOSITORY,
            title="Core",
            subentry_id="home-subentry-id",
            unique_id="universal-assistant/core",
        )
    ]


@pytest.fixture
def mock_config_entry(
    mock_subentries: list[ConfigSubentryDataWithId],
) -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="",
        domain=DOMAIN,
        data={CONF_ACCESS_TOKEN: MOCK_ACCESS_TOKEN},
        subentries_data=[*mock_subentries],
        minor_version=2,
    )


@pytest.fixture
def mock_setup_entry() -> Generator[None]:
    """Mock setting up a config entry."""
    with patch("universalassistant.components.github.async_setup_entry", return_value=None):
        yield


@pytest.fixture
def device_activation_event() -> asyncio.Event:
    """Fixture to provide an asyncio event for device activation."""
    return asyncio.Event()


@pytest.fixture
def github_device_client(
    hass: __HAC_KEEP__,
    device_activation_event: asyncio.Event,
) -> Generator[AsyncMock]:
    """Mock GitHub device client."""
    with patch(
        "universalassistant.components.github.config_flow.GitHubDeviceAPI",
        autospec=True,
    ) as github_client_mock:
        client = github_client_mock.return_value
        register_object = AsyncMock()
        register_object.data = GitHubLoginDeviceModel(
            load_json_object_fixture("device_register.json", DOMAIN)
        )
        client.register.return_value = register_object

        async def mock_api_device_activation(device_code) -> AsyncMock:
            # Simulate the device activation process
            await device_activation_event.wait()
            activate_object = AsyncMock()
            activate_object.data = GitHubLoginOauthModel(
                await async_load_json_object_fixture(
                    hass, "device_activate.json", DOMAIN
                )
            )
            return activate_object

        client.activation = mock_api_device_activation
        yield client


@pytest.fixture
def github_client(hass: __HAC_KEEP__) -> Generator[AsyncMock]:
    """Mock GitHub device client."""
    with (
        patch(
            "universalassistant.components.github.config_flow.GitHubAPI",
            autospec=True,
        ) as github_client_mock,
        patch("universalassistant.components.github.GitHubAPI", new=github_client_mock),
        patch(
            "universalassistant.components.github.diagnostics.GitHubAPI",
            new=github_client_mock,
        ),
    ):
        client = github_client_mock.return_value
        client.user.starred = AsyncMock(
            side_effect=[
                MagicMock(
                    is_last_page=False,
                    next_page_number=2,
                    last_page_number=2,
                    data=[MagicMock(full_name="universal-assistant/core")],
                ),
                MagicMock(
                    is_last_page=True,
                    data=[MagicMock(full_name="universal-assistant/frontend")],
                ),
            ]
        )
        client.user.repos = AsyncMock(
            side_effect=[
                MagicMock(
                    is_last_page=False,
                    next_page_number=2,
                    last_page_number=2,
                    data=[MagicMock(full_name="universal-assistant/operating-system")],
                ),
                MagicMock(
                    is_last_page=True,
                    data=[MagicMock(full_name="esphome/esphome")],
                ),
            ]
        )
        rate_limit_mock = AsyncMock()
        rate_limit_mock.data = GitHubRateLimitModel(
            load_json_object_fixture("rate_limit.json", DOMAIN)
        )
        client.rate_limit.return_value = rate_limit_mock
        graphql_mock = AsyncMock()
        graphql_mock.data = load_json_object_fixture("graphql.json", DOMAIN)
        client.graphql.return_value = graphql_mock
        user_response_mock = MagicMock()
        user_response_mock.data = GitHubAuthenticatedUserModel(
            load_json_object_fixture("user.json", DOMAIN)
        )
        client.user.get = AsyncMock(return_value=user_response_mock)
        client.repos.events.subscribe = AsyncMock()
        yield client
