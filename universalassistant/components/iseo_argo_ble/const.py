"""Constants for the ISEO Argo BLE Lock integration."""

from universalassistant.const import Platform

DOMAIN = "iseo_argo_ble"
PLATFORMS: list[Platform] = [Platform.LOCK]

# Config entry keys (CONF_ADDRESS and CONF_UUID come from universalassistant.const)
CONF_PRIV_SCALAR = "priv_scalar"

# Default user subtype (gateway)
DEFAULT_USER_SUBTYPE: int = 17  # UserSubType.BT_GATEWAY
