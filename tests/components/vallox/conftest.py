"""Common utilities for Vallox tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, load_json_object_fixture
from vallox_websocket_api import MetricData, MetricValue

from universalassistant.components.vallox.const import DOMAIN
from universalassistant.const import CONF_HOST, CONF_NAME
from universalassistant.core import UniversalAssistant

from . import TEST_HOST, TEST_NAME, setup_integration


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=TEST_NAME,
        data={CONF_HOST: TEST_HOST, CONF_NAME: TEST_NAME},
    )


@pytest.fixture
def default_metrics() -> dict[str, MetricValue]:
    """Return default Vallox metrics."""
    return load_json_object_fixture("metrics.json", DOMAIN)


@pytest.fixture
def metrics() -> dict[str, MetricValue]:
    """Return values that replace single entries of metrics.json.

    Tests override this fixture with @pytest.mark.parametrize("metrics", ...).
    """
    return {}


@pytest.fixture
def mock_vallox_client(
    default_metrics: dict[str, MetricValue],
    metrics: dict[str, MetricValue],
) -> Generator[AsyncMock]:
    """Return a mocked Vallox client used by both the integration and config flow."""
    with (
        patch("universalassistant.components.vallox.Vallox", autospec=True) as mock_class,
        patch("universalassistant.components.vallox.config_flow.Vallox", new=mock_class),
    ):
        client = mock_class.return_value
        client.fetch_metric_data.return_value = MetricData(default_metrics | metrics)
        yield client


@pytest.fixture
async def init_integration(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_vallox_client: AsyncMock,
) -> MockConfigEntry:
    """Set up the Vallox integration for testing."""
    await setup_integration(hass, mock_config_entry)
    return mock_config_entry


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "universalassistant.components.vallox.async_setup_entry", return_value=None
    ) as mock_setup_entry:
        yield mock_setup_entry
