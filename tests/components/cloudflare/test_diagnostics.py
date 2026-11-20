"""Test the Cloudflare diagnostics."""

from unittest.mock import MagicMock

import pycfdns
import pytest
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.cloudflare.const import DOMAIN
from universalassistant.components.cloudflare.services import CloudflareService
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant

from . import init_integration


@pytest.mark.usefixtures("location_info")
@pytest.mark.parametrize(
    "list_dns_records_side_effect",
    [
        pytest.param(None, id="success"),
        pytest.param(pycfdns.ComunicationException(), id="update_failed"),
    ],
)
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    cfupdate: MagicMock,
    snapshot: SnapshotAssertion,
    list_dns_records_side_effect: Exception | None,
) -> None:
    """Test diagnostics."""
    entry = await init_integration(hass)
    assert entry.state is ConfigEntryState.LOADED

    cfupdate.return_value.list_dns_records.side_effect = list_dns_records_side_effect
    await hass.services.async_call(
        DOMAIN, CloudflareService.UPDATE_RECORDS, {}, blocking=True
    )

    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
