"""Coordinator for the Namecheap DynamicDNS integration."""

from datetime import timedelta
import logging
from typing import override

from aiohttp import ClientError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_DOMAIN, CONF_HOST, CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .helpers import AuthFailed, update_namecheapdns

_LOGGER = logging.getLogger(__name__)


type NamecheapConfigEntry = ConfigEntry[NamecheapDnsUpdateCoordinator]


INTERVAL = timedelta(minutes=5)


class NamecheapDnsUpdateCoordinator(DataUpdateCoordinator[None]):
    """Namecheap DynamicDNS update coordinator."""

    config_entry: NamecheapConfigEntry

    def __init__(self, hass: __HAC_KEEP__, config_entry: NamecheapConfigEntry) -> None:
        """Initialize the Namecheap DynamicDNS update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=INTERVAL,
        )

        self.session = async_get_clientsession(hass)

    @override
    async def _async_update_data(self) -> None:
        """Update Namecheap DNS."""
        host = self.config_entry.data[CONF_HOST]
        domain = self.config_entry.data[CONF_DOMAIN]
        password = self.config_entry.data[CONF_PASSWORD]

        try:
            if not await update_namecheapdns(self.session, host, domain, password):
                raise UpdateFailed(
                    translation_domain=DOMAIN,
                    translation_key="update_failed",
                    translation_placeholders={"domain": f"{host}.{domain}"},
                )
        except AuthFailed as e:
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="authentication_failed",
                translation_placeholders={"domain": f"{host}.{domain}"},
            ) from e
        except ClientError as e:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
                translation_placeholders={"domain": f"{host}.{domain}"},
            ) from e
