"""Tests for the init."""

from typing import Any
from unittest.mock import Mock, patch

from pytest_universalassistant.common import MockUser

from universalassistant.components import onboarding
from universalassistant.components.onboarding import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from . import mock_storage

# Temporarily: if auth not active, always set onboarded=True


async def test_not_setup_views_if_onboarded(
    hass: UniversalAssistant, hass_storage: dict[str, Any]
) -> None:
    """Test if onboarding is done, we don't setup views."""
    mock_storage(hass_storage, {"done": onboarding.STEPS})

    with patch("universalassistant.components.onboarding.views.async_setup") as mock_setup:
        assert await async_setup_component(hass, DOMAIN, {})

    assert len(mock_setup.mock_calls) == 0
    assert onboarding.DOMAIN not in hass.data
    assert onboarding.async_is_onboarded(hass)


async def test_setup_views_if_not_onboarded(hass: UniversalAssistant) -> None:
    """Test if onboarding is not done, we setup views."""
    with patch(
        "universalassistant.components.onboarding.views.async_setup",
    ) as mock_setup:
        assert await async_setup_component(hass, DOMAIN, {})

    assert len(mock_setup.mock_calls) == 1
    assert onboarding.DOMAIN in hass.data

    assert not onboarding.async_is_onboarded(hass)


async def test_is_onboarded() -> None:
    """Test the is onboarded function."""
    hass = Mock()
    hass.data = {}

    assert onboarding.async_is_onboarded(hass)

    hass.data[onboarding.DOMAIN] = onboarding.OnboardingData([], True, {"done": []})
    assert onboarding.async_is_onboarded(hass)

    hass.data[onboarding.DOMAIN] = onboarding.OnboardingData([], False, {"done": []})
    assert not onboarding.async_is_onboarded(hass)


async def test_is_user_onboarded() -> None:
    """Test the is onboarded function."""
    hass = Mock()
    hass.data = {}

    assert onboarding.async_is_user_onboarded(hass)

    hass.data[onboarding.DOMAIN] = onboarding.OnboardingData([], True, {"done": []})
    assert onboarding.async_is_user_onboarded(hass)

    hass.data[onboarding.DOMAIN] = onboarding.OnboardingData(
        [], False, {"done": ["user"]}
    )
    assert onboarding.async_is_user_onboarded(hass)

    hass.data[onboarding.DOMAIN] = onboarding.OnboardingData([], False, {"done": []})
    assert not onboarding.async_is_user_onboarded(hass)


async def test_having_owner_finishes_user_step(
    hass: UniversalAssistant, hass_storage: dict[str, Any]
) -> None:
    """If owner user already exists, mark user step as complete."""
    MockUser(is_owner=True).add_to_hass(hass)

    with (
        patch("universalassistant.components.onboarding.views.async_setup") as mock_setup,
        patch.object(onboarding, "STEPS", [onboarding.STEP_USER]),
    ):
        assert await async_setup_component(hass, DOMAIN, {})

    assert len(mock_setup.mock_calls) == 0
    assert onboarding.DOMAIN not in hass.data
    assert onboarding.async_is_onboarded(hass)

    done = hass_storage[onboarding.STORAGE_KEY]["data"]["done"]
    assert onboarding.STEP_USER in done


async def test_migration(hass: UniversalAssistant, hass_storage: dict[str, Any]) -> None:
    """Test migrating onboarding to new version."""
    hass_storage[onboarding.STORAGE_KEY] = {"version": 1, "data": {"done": ["user"]}}
    assert await async_setup_component(hass, DOMAIN, {})
    assert onboarding.async_is_onboarded(hass)
