"""Test buttons."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockUser

from universalassistant.components import google_assistant as ga
from universalassistant.core import Context, UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.setup import async_setup_component

from .test_http import DUMMY_CONFIG

SYNC_BUTTON_ENTITY_ID = "button.google_home_synchronize_devices"


async def test_sync_button(hass: UniversalAssistant, hass_owner_user: MockUser) -> None:
    """Test sync button."""

    await async_setup_component(
        hass,
        ga.DOMAIN,
        {"google_assistant": DUMMY_CONFIG},
    )

    await hass.async_block_till_done()

    state = hass.states.get(SYNC_BUTTON_ENTITY_ID)
    assert state

    config_entry = hass.config_entries.async_entries("google_assistant")[0]
    google_config: ga.GoogleConfig = config_entry.runtime_data

    with patch.object(google_config, "async_sync_entities") as mock_sync_entities:
        mock_sync_entities.return_value = 200
        context = Context(user_id=hass_owner_user.id)
        await hass.services.async_call(
            "button",
            "press",
            {"entity_id": SYNC_BUTTON_ENTITY_ID},
            blocking=True,
            context=context,
        )
        mock_sync_entities.assert_called_once_with(hass_owner_user.id)

        mock_sync_entities.return_value = 400
        with pytest.raises(UniversalAssistantError):
            await hass.services.async_call(
                "button",
                "press",
                {"entity_id": SYNC_BUTTON_ENTITY_ID},
                blocking=True,
                context=context,
            )
