"""Test the SFR Box diagnostics."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from sfrbox_api.models import SystemInfo
from syrupy.assertion import SnapshotAssertion

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant

pytestmark = pytest.mark.usefixtures(
    "dsl_get_info", "ftth_get_info", "system_get_info", "voip_get_info", "wan_get_info"
)


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with (
        patch("universalassistant.components.sfr_box.PLATFORMS", []),
        patch("universalassistant.components.sfr_box.coordinator.SFRBox.authenticate"),
    ):
        yield


@pytest.mark.parametrize(
    ("net_infra", "patch_to_none"),
    [("adsl", "ftth_get_info"), ("ftth", "dsl_get_info")],
)
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    config_entry_with_auth: ConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    system_get_info: SystemInfo,
    net_infra: str,
    patch_to_none: str,
) -> None:
    """Test config entry diagnostics."""
    system_get_info.net_infra = net_infra
    await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
    await hass.async_block_till_done()

    with patch(
        f"universalassistant.components.sfr_box.coordinator.SFRBox.{patch_to_none}",
        return_value=None,
    ):
        assert (
            await get_diagnostics_for_config_entry(
                hass, hass_client, config_entry_with_auth
            )
            == snapshot
        )
