"""Fixtures for the Sensibo integration."""

from collections.abc import AsyncGenerator, Generator
import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

from pysensibo import SensiboClient, SensiboData
import pytest
from pytest_universalassistant.common import MockConfigEntry, load_fixture
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.sensibo.const import DOMAIN, PLATFORMS
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from . import ENTRY_CONFIG


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.sensibo.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(name="load_platforms")
async def patch_platform_constant() -> list[Platform]:
    """Return list of platforms to load."""
    return PLATFORMS


@pytest.fixture
async def load_int(
    hass: __HAC_KEEP__,
    mock_client: SensiboClient,
    load_platforms: list[Platform],
) -> MockConfigEntry:
    """Set up the Sensibo integration."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=ENTRY_CONFIG,
        entry_id="1",
        unique_id="firstnamelastname",
        version=2,
    )

    config_entry.add_to_hass(hass)

    with patch("universalassistant.components.sensibo.PLATFORMS", load_platforms):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    return config_entry


@pytest.fixture(name="mock_client")
async def get_client(
    hass: __HAC_KEEP__,
    get_data: tuple[SensiboData, dict[str, Any], dict[str, Any]],
) -> AsyncGenerator[MagicMock]:
    """Mock SensiboClient."""

    with (
        patch(
            "universalassistant.components.sensibo.coordinator.SensiboClient",
            autospec=True,
        ) as mock_client,
        patch("universalassistant.components.sensibo.util.SensiboClient", new=mock_client),
    ):
        client = mock_client.return_value
        client.async_get_devices_data.return_value = get_data[0]
        client.async_get_me.return_value = get_data[1]
        client.async_get_devices.return_value = get_data[2]
        yield client


@pytest.fixture(name="get_data")
async def get_data_from_library(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    load_json: tuple[dict[str, Any], dict[str, Any]],
) -> AsyncGenerator[tuple[SensiboData, dict[str, Any], dict[str, Any]]]:
    """Get data from api."""
    client = SensiboClient("1234567890", aioclient_mock.create_session(hass.loop))
    with patch.object(
        client,
        "async_get_me",
        return_value=load_json[1],
    ):
        me = await client.async_get_me()
    with patch.object(
        client,
        "async_get_devices",
        return_value=load_json[0],
    ):
        data = await client.async_get_devices_data()
        raw_data = await client.async_get_devices()
    yield (data, me, raw_data)
    await client._session.close()


@pytest.fixture(name="load_json")
def load_json_from_fixture(
    load_data: tuple[str, str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load fixture with json data and return."""
    json_data: dict[str, Any] = json.loads(load_data[0])
    json_me: dict[str, Any] = json.loads(load_data[1])
    return (json_data, json_me)


@pytest.fixture(name="load_data", scope="package")
def load_data_from_fixture() -> tuple[str, str]:
    """Load fixture with fixture data and return."""
    return (load_fixture("data.json", "sensibo"), load_fixture("me.json", "sensibo"))
