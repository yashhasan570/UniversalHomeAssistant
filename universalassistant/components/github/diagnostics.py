"""Diagnostics support for the GitHub integration."""

from typing import Any

from aiogithubapi import GitHubAPI, GitHubException

from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import (
    SERVER_SOFTWARE,
    async_get_clientsession,
)

from .coordinator import GithubConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    config_entry: GithubConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data: dict[str, Any] = {}
    client = GitHubAPI(
        token=config_entry.data[CONF_ACCESS_TOKEN],
        session=async_get_clientsession(hass),
        client_name=SERVER_SOFTWARE,
    )

    try:
        rate_limit_response = await client.rate_limit()
    except GitHubException as err:
        data["rate_limit"] = {"error": str(err)}
    else:
        data["rate_limit"] = rate_limit_response.data.as_dict

    repositories = config_entry.runtime_data.repositories
    data["repositories"] = {}

    for coordinator in repositories.values():
        data["repositories"][coordinator.data["full_name"]] = coordinator.data

    return data
