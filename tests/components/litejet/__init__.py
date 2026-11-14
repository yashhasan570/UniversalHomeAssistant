"""Tests for the litejet component."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components import scene, switch
from universalassistant.components.litejet.const import DOMAIN
from universalassistant.const import CONF_PORT
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


async def async_init_integration(
    hass: UniversalAssistant, use_switch: bool = False, use_scene: bool = False
) -> MockConfigEntry:
    """Set up the LiteJet integration in Universal Universal Home Assistant."""

    registry = er.async_get(hass)

    entry_data = {CONF_PORT: "/dev/mock"}

    entry = MockConfigEntry(
        domain=DOMAIN, unique_id=entry_data[CONF_PORT], data=entry_data
    )

    if use_switch:
        registry.async_get_or_create(
            switch.DOMAIN,
            DOMAIN,
            f"{entry.entry_id}_1",
            suggested_object_id="mock_switch_1",
            disabled_by=None,
        )
        registry.async_get_or_create(
            switch.DOMAIN,
            DOMAIN,
            f"{entry.entry_id}_2",
            suggested_object_id="mock_switch_2",
            disabled_by=None,
        )

    if use_scene:
        registry.async_get_or_create(
            scene.DOMAIN,
            DOMAIN,
            f"{entry.entry_id}_1",
            suggested_object_id="litejet_mock_scene_1",
            disabled_by=None,
        )

    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry
