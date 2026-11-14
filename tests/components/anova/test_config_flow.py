"""Test Anova config flow."""

from unittest.mock import patch

from anova_wifi import AnovaApi, InvalidLogin

from universalassistant import config_entries
from universalassistant.components.anova.const import DOMAIN
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from . import CONF_INPUT


async def test_flow_user(hass: __HAC_KEEP__, anova_api: AnovaApi) -> None:
    """Test user initialized flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=CONF_INPUT,
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_USERNAME: "sample@gmail.com",
        CONF_PASSWORD: "sample",
    }
    assert result["result"].unique_id == "sample@gmail.com"


async def test_flow_wrong_login(hass: __HAC_KEEP__) -> None:
    """Test incorrect login throwing error."""
    with patch(
        "universalassistant.components.anova.config_flow.AnovaApi.authenticate",
        side_effect=InvalidLogin,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONF_INPUT,
        )
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"base": "invalid_auth"}

    with (
        patch("universalassistant.components.anova.config_flow.AnovaApi.authenticate"),
        patch("universalassistant.components.anova.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONF_INPUT,
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_flow_unknown_error(hass: __HAC_KEEP__) -> None:
    """Test unknown error throwing error."""
    with patch(
        "universalassistant.components.anova.config_flow.AnovaApi.authenticate",
        side_effect=Exception(),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONF_INPUT,
        )
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"base": "unknown"}

    with (
        patch("universalassistant.components.anova.config_flow.AnovaApi.authenticate"),
        patch("universalassistant.components.anova.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONF_INPUT,
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY
