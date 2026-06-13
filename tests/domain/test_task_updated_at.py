from datetime import datetime, timedelta, timezone

import pytest

from assistant_core.domain.entities import task as task_module
from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority


@pytest.fixture
def fake_datetime(monkeypatch: pytest.MonkeyPatch):
    class FakeDateTime:
        current = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        @classmethod
        def now(cls, tz=None):
            value = cls.current

            if tz is not None and value.tzinfo is None:
                value = value.replace(tzinfo=tz)

            cls.current = cls.current + timedelta(seconds=1)
            return value

    monkeypatch.setattr(task_module, "datetime", FakeDateTime)

    return FakeDateTime


def test_created_task_has_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")

    assert task.updated_at is not None
    assert task.updated_at == task.created_at


def test_rename_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Old title")
    old_updated_at = task.updated_at

    task.rename("New title")

    assert task.updated_at > old_updated_at


def test_change_description_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")
    old_updated_at = task.updated_at

    task.change_description("After work")

    assert task.updated_at > old_updated_at


def test_change_priority_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")
    old_updated_at = task.updated_at

    task.change_priority(TaskPriority.HIGH)

    assert task.updated_at > old_updated_at


def test_complete_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")
    old_updated_at = task.updated_at

    task.complete()

    assert task.updated_at > old_updated_at
    assert task.updated_at == task.completed_at


def test_reopen_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")
    task.complete()
    old_updated_at = task.updated_at

    task.reopen()

    assert task.updated_at > old_updated_at
    assert task.completed_at is None


def test_cancel_updates_updated_at(fake_datetime) -> None:
    task = Task(title="Buy milk")
    old_updated_at = task.updated_at

    task.cancel()

    assert task.updated_at > old_updated_at
