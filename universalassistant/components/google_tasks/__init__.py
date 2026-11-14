"""The Google Tasks integration."""

import asyncio

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_entry_oauth2_flow

from . import api
from .const import DOMAIN
from .coordinator import GoogleTasksConfigEntry, TaskUpdateCoordinator
from .exceptions import GoogleTasksApiError

__all__ = [
    "DOMAIN",
]

PLATFORMS: list[Platform] = [Platform.TODO]


async def async_setup_entry(hass: UniversalAssistant, entry: GoogleTasksConfigEntry) -> None:
    """Set up Google Tasks from a config entry."""
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )
    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    auth = api.AsyncConfigEntryAuth(hass, session)
    await auth.async_get_access_token()

    try:
        task_lists = await auth.list_task_lists()
    except GoogleTasksApiError as err:
        raise ConfigEntryNotReady from err

    coordinators = [
        TaskUpdateCoordinator(
            hass,
            entry,
            auth,
            task_list["id"],
            task_list["title"],
        )
        for task_list in task_lists
    ]
    # Refresh all coordinators in parallel
    await asyncio.gather(
        *(
            coordinator.async_config_entry_first_refresh()
            for coordinator in coordinators
        )
    )
    entry.runtime_data = coordinators

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: GoogleTasksConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
