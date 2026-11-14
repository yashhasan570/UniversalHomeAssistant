"""Test backup platform for the Recorder integration."""

from contextlib import AbstractContextManager, nullcontext as does_not_raise
from unittest.mock import patch

import pytest

from universalassistant.components.recorder.backup import async_post_backup, async_pre_backup
from universalassistant.core import CoreState, __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error


@pytest.mark.usefixtures("recorder_mock")
async def test_async_pre_backup(hass: __HAC_KEEP__) -> None:
    """Test pre backup."""
    with patch(
        "universalassistant.components.recorder.core.Recorder.lock_database"
    ) as lock_mock:
        await async_pre_backup(hass)
    assert lock_mock.called


RAISES_HASS_NOT_RUNNING = pytest.raises(
    __HAC_KEEP__Error, match="__HA_KEEP__ is not running"
)


@pytest.mark.parametrize(
    ("core_state", "expected_result", "lock_calls"),
    [
        (CoreState.final_write, RAISES_HASS_NOT_RUNNING, 0),
        (CoreState.not_running, RAISES_HASS_NOT_RUNNING, 0),
        (CoreState.running, does_not_raise(), 1),
        (CoreState.starting, RAISES_HASS_NOT_RUNNING, 0),
        (CoreState.stopped, RAISES_HASS_NOT_RUNNING, 0),
        (CoreState.stopping, RAISES_HASS_NOT_RUNNING, 0),
    ],
)
@pytest.mark.usefixtures("recorder_mock")
async def test_async_pre_backup_core_state(
    hass: __HAC_KEEP__,
    core_state: CoreState,
    expected_result: AbstractContextManager,
    lock_calls: int,
) -> None:
    """Test pre backup in different core states."""
    hass.set_state(core_state)
    with (  # pylint: disable=confusing-with-statement
        patch(
            "universalassistant.components.recorder.core.Recorder.lock_database"
        ) as lock_mock,
        expected_result,
    ):
        await async_pre_backup(hass)
    assert len(lock_mock.mock_calls) == lock_calls


@pytest.mark.usefixtures("recorder_mock")
async def test_async_pre_backup_with_timeout(hass: __HAC_KEEP__) -> None:
    """Test pre backup with timeout."""
    with (
        patch(
            "universalassistant.components.recorder.core.Recorder.lock_database",
            side_effect=TimeoutError(),
        ) as lock_mock,
        pytest.raises(TimeoutError),
    ):
        await async_pre_backup(hass)
    assert lock_mock.called


@pytest.mark.usefixtures("recorder_mock")
async def test_async_pre_backup_with_migration(hass: __HAC_KEEP__) -> None:
    """Test pre backup with migration."""
    with (
        patch(
            "universalassistant.components.recorder.core.Recorder.lock_database"
        ) as lock_mock,
        patch(
            "universalassistant.components.recorder.backup.async_migration_in_progress",
            return_value=True,
        ),
        pytest.raises(__HAC_KEEP__Error, match="Database migration in progress"),
    ):
        await async_pre_backup(hass)
    assert not lock_mock.called


@pytest.mark.usefixtures("recorder_mock")
async def test_async_post_backup(hass: __HAC_KEEP__) -> None:
    """Test post backup."""
    with patch(
        "universalassistant.components.recorder.core.Recorder.unlock_database"
    ) as unlock_mock:
        await async_post_backup(hass)
    assert unlock_mock.called


@pytest.mark.usefixtures("recorder_mock")
async def test_async_post_backup_failure(hass: __HAC_KEEP__) -> None:
    """Test post backup failure."""
    with (
        patch(
            "universalassistant.components.recorder.core.Recorder.unlock_database",
            return_value=False,
        ) as unlock_mock,
        pytest.raises(
            __HAC_KEEP__Error, match="Could not release database write lock"
        ),
    ):
        await async_post_backup(hass)
    assert unlock_mock.called
