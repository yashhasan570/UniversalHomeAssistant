"""The tests for Alarm control panel platforms."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant


async def help_async_setup_entry_init(
    hass: UniversalAssistant, config_entry: ConfigEntry
) -> None:
    """Set up test config entry."""
    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )


async def help_async_unload_entry(
    hass: UniversalAssistant, config_entry: ConfigEntry
) -> None:
    """Unload test config emntry."""
    await hass.config_entries.async_unload_platforms_or_raise(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )
