"""Testing for ScreenLogic diagnostics."""

from unittest.mock import DEFAULT, patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from screenlogicpy import ScreenLogicGateway
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import device_registry as dr

from . import (
    DATA_FULL_CHEM,
    GATEWAY_DISCOVERY_IMPORT_PATH,
    MOCK_ADAPTER_MAC,
    stub_async_connect,
)


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    device_registry: dr.DeviceRegistry,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    mock_config_entry.add_to_hass(hass)

    device_registry.async_get_or_create(
        config_entry_id=mock_config_entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, MOCK_ADAPTER_MAC)},
    )
    with (
        patch(
            GATEWAY_DISCOVERY_IMPORT_PATH,
            return_value={},
        ),
        patch.multiple(
            ScreenLogicGateway,
            async_connect=lambda *args, **kwargs: stub_async_connect(
                DATA_FULL_CHEM, *args, **kwargs
            ),
            is_connected=True,
            _async_connected_request=DEFAULT,
            get_debug=lambda self: {},
        ),
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        diag = await get_diagnostics_for_config_entry(
            hass, hass_client, mock_config_entry
        )

    assert diag == snapshot(exclude=props("created_at", "modified_at"))
