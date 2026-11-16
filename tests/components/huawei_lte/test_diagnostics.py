"""Test huawei_lte diagnostics."""

from unittest.mock import MagicMock, patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.huawei_lte.const import DOMAIN
from universalassistant.const import CONF_URL
from universalassistant.core import UniversalAssistant

from . import magic_client


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    huawei_lte = MockConfigEntry(
        domain=DOMAIN, data={CONF_URL: "http://huawei-lte.example.com"}
    )
    huawei_lte.add_to_hass(hass)
    with (
        patch("universalassistant.components.huawei_lte.Connection", MagicMock()),
        patch(
            "universalassistant.components.huawei_lte.Client", return_value=magic_client()
        ),
    ):
        await hass.config_entries.async_setup(huawei_lte.entry_id)
    await hass.async_block_till_done()

    result = await get_diagnostics_for_config_entry(hass, hass_client, huawei_lte)
    assert result == snapshot(exclude=props("entry_id", "created_at", "modified_at"))
