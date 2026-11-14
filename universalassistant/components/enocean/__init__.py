"""Support for EnOcean devices."""

from enocean_async import Gateway
import probatio

from universalassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from universalassistant.const import CONF_DEVICE
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, SIGNAL_RECEIVE_MESSAGE, SIGNAL_SEND_MESSAGE

type EnOceanConfigEntry = ConfigEntry[Gateway]

CONFIG_SCHEMA = probatio.Schema(
    {DOMAIN: probatio.Schema({probatio.Required(CONF_DEVICE): cv.string})},
    extra=probatio.ALLOW_EXTRA,
)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the EnOcean component."""
    # support for text-based configuration (legacy)
    if DOMAIN not in config:
        return True

    if hass.config_entries.async_entries(DOMAIN):
        # We can only have one gateway. If there is already one in the config,
        # there is no need to import the yaml based config.
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=config[DOMAIN]
        )
    )

    return True


async def async_setup_entry(
    hass: UniversalAssistant, config_entry: EnOceanConfigEntry
) -> None:
    """Set up an EnOcean gateway for the given entry."""
    gateway = Gateway(port=config_entry.data[CONF_DEVICE])

    gateway.add_erp1_received_callback(
        lambda packet: async_dispatcher_send(hass, SIGNAL_RECEIVE_MESSAGE, packet)
    )

    try:
        await gateway.start()
    except ConnectionError as err:
        gateway.stop()
        raise ConfigEntryNotReady(f"Failed to start EnOcean gateway: {err}") from err

    config_entry.runtime_data = gateway

    config_entry.async_on_unload(
        async_dispatcher_connect(hass, SIGNAL_SEND_MESSAGE, gateway.send_esp3_packet)
    )


async def async_unload_entry(
    hass: UniversalAssistant, config_entry: EnOceanConfigEntry
) -> None:
    """Unload EnOcean config entry: stop the gateway."""

    config_entry.runtime_data.stop()
