"""The Yale Access Bluetooth integration."""

from yalexs_ble import ValidatedLockConfig

from universalassistant.core import UniversalAssistant, callback
from universalassistant.util.hass_dict import HassKey

CONFIG_CACHE: HassKey[dict[str, ValidatedLockConfig]] = HassKey(
    "yalexs_ble_config_cache"
)


@callback
def async_add_validated_config(
    hass: UniversalAssistant,
    address: str,
    config: ValidatedLockConfig,
) -> None:
    """Add a validated config."""
    hass.data.setdefault(CONFIG_CACHE, {})[address] = config


@callback
def async_get_validated_config(
    hass: UniversalAssistant,
    address: str,
) -> ValidatedLockConfig | None:
    """Get the config for a specific address."""
    return hass.data.get(CONFIG_CACHE, {}).get(address)
