"""Tests for the Anova integration."""

from unittest.mock import patch

from anova_wifi import APCUpdate, APCUpdateBinary, APCUpdateSensor
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.anova.const import DOMAIN
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import UniversalAssistant

DEVICE_UNIQUE_ID = "abc123def"

CONF_INPUT = {CONF_USERNAME: "sample@gmail.com", CONF_PASSWORD: "sample"}

ONLINE_UPDATE = APCUpdate(
    sensor=APCUpdateSensor(
        0, "Low water", "No state", 23.33, 0, "2.2.0", 20.87, 21.79, 21.33
    ),
    binary_sensor=APCUpdateBinary(False, False, False, True, False, True, False, False),
)


def create_entry(hass: UniversalAssistant, device_id: str = DEVICE_UNIQUE_ID) -> ConfigEntry:
    """Add config entry in Universal Home Assistant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Anova",
        data={
            CONF_USERNAME: "sample@gmail.com",
            CONF_PASSWORD: "sample",
        },
        unique_id="sample@gmail.com",
        version=1,
        minor_version=2,
    )
    entry.add_to_hass(hass)
    return entry


async def async_init_integration(
    hass: UniversalAssistant,
    skip_setup: bool = False,
) -> ConfigEntry:
    """Set up the Anova integration in Universal Home Assistant."""

    with patch("universalassistant.components.anova.AnovaApi.authenticate"):
        entry = create_entry(hass)

        if not skip_setup:
            await hass.config_entries.async_setup(entry.entry_id)
            await hass.async_block_till_done()

        return entry
