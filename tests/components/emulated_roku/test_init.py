"""Test emulated_roku component setup process."""

from unittest.mock import AsyncMock, Mock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import emulated_roku
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_config_required_fields(hass: UniversalAssistant) -> None:
    """Test that configuration is successful with required fields."""
    with (
        patch.object(emulated_roku, "configured_servers", return_value=[]),
        patch(
            "universalassistant.components.emulated_roku.binding.EmulatedRokuServer",
            return_value=Mock(start=AsyncMock(), close=AsyncMock()),
        ),
    ):
        assert (
            await async_setup_component(
                hass,
                emulated_roku.DOMAIN,
                {
                    emulated_roku.DOMAIN: {
                        emulated_roku.CONF_SERVERS: [
                            {
                                emulated_roku.CONF_NAME: "Emulated Roku Test",
                                emulated_roku.CONF_LISTEN_PORT: 8060,
                            }
                        ]
                    }
                },
            )
            is True
        )


async def test_config_already_registered_not_configured(hass: UniversalAssistant) -> None:
    """Test that an already registered name causes the entry to be ignored."""
    with (
        patch(
            "universalassistant.components.emulated_roku.binding.EmulatedRokuServer",
            return_value=Mock(start=AsyncMock(), close=AsyncMock()),
        ) as instantiate,
        patch.object(
            emulated_roku, "configured_servers", return_value=["Emulated Roku Test"]
        ),
    ):
        assert (
            await async_setup_component(
                hass,
                emulated_roku.DOMAIN,
                {
                    emulated_roku.DOMAIN: {
                        emulated_roku.CONF_SERVERS: [
                            {
                                emulated_roku.CONF_NAME: "Emulated Roku Test",
                                emulated_roku.CONF_LISTEN_PORT: 8060,
                            }
                        ]
                    }
                },
            )
            is True
        )

    assert len(instantiate.mock_calls) == 0


async def test_setup_entry_successful(hass: UniversalAssistant) -> None:
    """Test setup entry is successful."""
    entry = MockConfigEntry(
        domain=emulated_roku.DOMAIN,
        data={
            emulated_roku.CONF_NAME: "Emulated Roku Test",
            emulated_roku.CONF_LISTEN_PORT: 8060,
            emulated_roku.CONF_HOST_IP: "1.2.3.5",
            emulated_roku.CONF_ADVERTISE_IP: "1.2.3.4",
            emulated_roku.CONF_ADVERTISE_PORT: 8071,
            emulated_roku.CONF_UPNP_BIND_MULTICAST: False,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.emulated_roku.binding.EmulatedRokuServer",
        return_value=Mock(start=AsyncMock(), close=AsyncMock()),
    ) as instantiate:
        assert await hass.config_entries.async_setup(entry.entry_id) is True

    assert len(instantiate.mock_calls) == 1


async def test_setup_entry_failed(hass: UniversalAssistant) -> None:
    """Test setup entry fails when the server can't be set up."""
    entry = MockConfigEntry(
        domain=emulated_roku.DOMAIN,
        data={
            emulated_roku.CONF_NAME: "Emulated Roku Test",
            emulated_roku.CONF_LISTEN_PORT: 8060,
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.emulated_roku.EmulatedRoku.setup",
        return_value=False,
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.reason == "Failed to set up Emulated Roku Emulated Roku Test"


async def test_unload_entry(hass: UniversalAssistant) -> None:
    """Test being able to unload an entry."""
    entry = MockConfigEntry(
        domain=emulated_roku.DOMAIN,
        data={
            "name": "Emulated Roku Test",
            "listen_port": 8060,
            emulated_roku.CONF_HOST_IP: "1.2.3.5",
        },
    )
    entry.add_to_hass(hass)

    with patch(
        "universalassistant.components.emulated_roku.binding.EmulatedRokuServer",
        return_value=Mock(start=AsyncMock(), close=AsyncMock()),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id) is True

    await hass.async_block_till_done()

    assert await hass.config_entries.async_unload(entry.entry_id)
