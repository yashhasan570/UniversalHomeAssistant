"""Tests for the TP-Link LTE integration."""

from universalassistant.components.tplink_lte import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import issue_registry as ir
from universalassistant.setup import async_setup_component


async def test_tplink_lte_repair_issue(
    hass: __HAC_KEEP__, issue_registry: ir.IssueRegistry
) -> None:
    """Test the TP-Link LTE repair issue is created on setup."""
    assert await async_setup_component(
        hass,
        DOMAIN,
        {DOMAIN: [{"host": "192.168.0.1", "password": "secret"}]},
    )
    await hass.async_block_till_done()

    assert issue_registry.async_get_issue(DOMAIN, DOMAIN)
    issue = issue_registry.async_get_issue(DOMAIN, DOMAIN)
    assert issue.severity == ir.IssueSeverity.ERROR
    assert issue.translation_key == "integration_removed"
