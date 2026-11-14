"""Casper Glow session fixtures."""

from collections.abc import Awaitable, Callable, Generator
from unittest.mock import MagicMock, patch

from pycasperglow import GlowState
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.casper_glow.const import DOMAIN
from universalassistant.const import CONF_ADDRESS
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.device_registry import format_mac

from . import CASPER_GLOW_DISCOVERY_INFO, setup_integration


@pytest.fixture(autouse=True)
def mock_bluetooth(enable_bluetooth: None) -> None:
    """Auto mock bluetooth."""


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a Casper Glow config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Jar",
        data={CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address},
        unique_id=format_mac(CASPER_GLOW_DISCOVERY_INFO.address),
    )


@pytest.fixture
def mock_casper_glow() -> Generator[MagicMock]:
    """Mock a CasperGlow device."""
    with (
        patch(
            "universalassistant.components.casper_glow.CasperGlow",
            autospec=True,
        ) as mock_device_class,
        patch(
            "universalassistant.components.casper_glow.config_flow.CasperGlow",
            new=mock_device_class,
        ),
    ):
        mock_device = mock_device_class.return_value
        mock_device.address = CASPER_GLOW_DISCOVERY_INFO.address
        mock_device.state = GlowState()
        yield mock_device


@pytest.fixture
def fire_callbacks(
    hass: UniversalAssistant,
    mock_casper_glow: MagicMock,
) -> Callable[[GlowState], Awaitable[None]]:
    """Return a helper that fires all registered device callbacks with a given state."""

    async def _fire(state: GlowState) -> None:
        for cb in (
            call[0][0] for call in mock_casper_glow.register_callback.call_args_list
        ):
            cb(state)
        await hass.async_block_till_done()

    return _fire


@pytest.fixture
async def config_entry(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_casper_glow: MagicMock,
) -> MockConfigEntry:
    """Set up a Casper Glow config entry."""
    await setup_integration(hass, mock_config_entry)
    return mock_config_entry
