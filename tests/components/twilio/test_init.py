"""Test the init file of Twilio."""

from unittest.mock import patch

from pytest_universalassistant.typing import ClientSessionGenerator

from universalassistant import config_entries
from universalassistant.components import twilio
from universalassistant.components.twilio import DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.core_config import async_process_ha_core_config
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.setup import async_setup_component


async def test_config_flow_registers_webhook(
    hass: UniversalAssistant, hass_client_no_auth: ClientSessionGenerator
) -> None:
    """Test setting up Twilio and sending webhook."""
    await async_process_ha_core_config(
        hass,
        {"internal_url": "http://example.local:8123"},
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM, result

    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    webhook_id = result["result"].data["webhook_id"]

    twilio_events = []

    @callback
    def handle_event(event):
        """Handle Twilio event."""
        twilio_events.append(event)

    hass.bus.async_listen(twilio.RECEIVED_DATA, handle_event)

    client = await hass_client_no_auth()
    await client.post(f"/api/webhook/{webhook_id}", data={"hello": "twilio"})

    assert len(twilio_events) == 1
    assert twilio_events[0].data["webhook_id"] == webhook_id
    assert twilio_events[0].data["hello"] == "twilio"


async def test_get_client(hass: UniversalAssistant) -> None:
    """Test the client created from the YAML configuration is returned."""
    with patch("universalassistant.components.twilio.Client") as mock_client:
        assert await async_setup_component(
            hass, DOMAIN, {DOMAIN: {"account_sid": "sid", "auth_token": "token"}}
        )
    mock_client.assert_called_once_with("sid", "token")
    assert twilio.get_client(hass) is mock_client.return_value
