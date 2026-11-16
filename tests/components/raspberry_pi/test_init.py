"""Test the Raspberry Pi integration."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, MockModule, mock_integration

from universalassistant.components.hassio import DOMAIN as HASSIO_DOMAIN, HassioNotReadyError
from universalassistant.components.raspberry_pi.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
def mock_rpi_power():
    """Mock the rpi_power integration."""
    with patch(
        "universalassistant.components.rpi_power.async_setup_entry",
        return_value=None,
    ):
        yield


async def test_setup_entry(hass: UniversalAssistant) -> None:
    """Test setup of a config entry."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Raspberry Pi",
    )
    config_entry.add_to_hass(hass)
    assert not hass.config_entries.async_entries("rpi_power")
    with (
        patch(
            "universalassistant.components.raspberry_pi.get_os_info",
            return_value={"board": "rpi"},
        ) as mock_get_os_info,
        patch("universalassistant.components.rpi_power.config_flow.new_under_voltage"),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert len(mock_get_os_info.mock_calls) == 1

    assert len(hass.config_entries.async_entries("rpi_power")) == 1


async def test_setup_entry_no_hassio(hass: UniversalAssistant) -> None:
    """Test setup of a config entry without hassio."""
    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Raspberry Pi",
    )
    config_entry.add_to_hass(hass)
    assert len(hass.config_entries.async_entries()) == 1

    with patch("universalassistant.components.raspberry_pi.get_os_info") as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 0
    assert len(hass.config_entries.async_entries()) == 0


async def test_setup_entry_wrong_board(hass: UniversalAssistant) -> None:
    """Test setup of a config entry with wrong board type."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Raspberry Pi",
    )
    config_entry.add_to_hass(hass)
    assert len(hass.config_entries.async_entries()) == 1

    with patch(
        "universalassistant.components.raspberry_pi.get_os_info",
        return_value={"board": "generic-x86-64"},
    ) as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 1
    assert len(hass.config_entries.async_entries()) == 0


@pytest.mark.parametrize(
    ("hassio", "board", "reason"),
    [
        pytest.param(
            False,
            None,
            "Universal Home Assistant is not running on Universal Home Assistant OS, the Raspberry Pi"
            " entry will be removed",
            id="no_hassio",
        ),
        pytest.param(
            True,
            "generic-x86-64",
            "Universal Home Assistant is not running on a Raspberry Pi (generic-x86-64), the"
            " Raspberry Pi entry will be removed",
            id="wrong_board",
        ),
    ],
)
async def test_setup_entry_error_reason(
    hass: UniversalAssistant, hassio: bool, board: str | None, reason: str
) -> None:
    """Test the setup error reason when the entry is about to be removed."""
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Raspberry Pi",
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.raspberry_pi.is_hassio",
            return_value=hassio,
        ),
        patch(
            "universalassistant.components.raspberry_pi.get_os_info",
            return_value={"board": board},
        ),
        patch.object(hass.config_entries, "async_remove", AsyncMock()) as mock_remove,
    ):
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_ERROR
    assert config_entry.reason == reason
    mock_remove.assert_awaited_once_with(config_entry.entry_id)


async def test_setup_entry_wait_hassio(hass: UniversalAssistant) -> None:
    """Test setup of a config entry when hassio has not fetched os_info."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="Raspberry Pi",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "universalassistant.components.raspberry_pi.get_os_info",
        side_effect=HassioNotReadyError,
    ) as mock_get_os_info:
        assert not await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(mock_get_os_info.mock_calls) == 1
    assert config_entry.state is ConfigEntryState.SETUP_RETRY
