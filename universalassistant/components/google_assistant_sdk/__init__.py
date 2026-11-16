"""Support for Google Assistant SDK."""

from universalassistant.const import CONF_NAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .helpers import (
    GoogleAssistantSDKAudioView,
    GoogleAssistantSDKConfigEntry,
    GoogleAssistantSDKRuntimeData,
    InMemoryStorage,
)
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS = [Platform.CONVERSATION]


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up Google Assistant SDK component."""
    hass.async_create_task(
        discovery.async_load_platform(
            hass, Platform.NOTIFY, DOMAIN, {CONF_NAME: DOMAIN}, config
        )
    )

    async_setup_services(hass)

    return True


async def async_setup_entry(
    hass: UniversalAssistant, entry: GoogleAssistantSDKConfigEntry
) -> None:
    """Set up Google Assistant SDK from a config entry."""
    implementation = await async_get_config_entry_implementation(hass, entry)
    session = OAuth2Session(hass, entry, implementation)
    await session.async_ensure_token_valid()

    mem_storage = InMemoryStorage(hass)
    hass.http.register_view(GoogleAssistantSDKAudioView(mem_storage))

    entry.runtime_data = GoogleAssistantSDKRuntimeData(
        session=session, mem_storage=mem_storage
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: GoogleAssistantSDKConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
