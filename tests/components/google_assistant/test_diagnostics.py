"""Test diagnostics."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant import setup
from universalassistant.components import google_assistant as ga, switch
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from .test_http import DUMMY_CONFIG


@pytest.fixture(autouse=True)
async def switch_only() -> None:
    """Enable only the switch platform."""
    with patch(
        "universalassistant.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.SWITCH],
    ):
        yield


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics v1."""

    await async_setup_component(hass, "universalassistant", {})
    await setup.async_setup_component(
        hass, switch.DOMAIN, {"switch": [{"platform": "demo"}]}
    )

    await async_setup_component(
        hass,
        ga.DOMAIN,
        {"google_assistant": DUMMY_CONFIG},
    )
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_entries("google_assistant")[0]
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(exclude=props("entry_id", "created_at", "modified_at"))
