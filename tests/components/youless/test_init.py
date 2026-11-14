"""Test the setup of the Youless integration."""

from universalassistant import setup
from universalassistant.components.youless.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import init_component


async def test_async_setup_entry(hass: UniversalAssistant) -> None:
    """Check if the setup of the integration succeeds."""

    entry = await init_component(hass)

    assert await setup.async_setup_component(hass, DOMAIN, {})
    assert entry.state is ConfigEntryState.LOADED
    assert len(hass.states.async_entity_ids()) == 23
