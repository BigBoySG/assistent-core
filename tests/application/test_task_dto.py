from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from assistant_core.application.dto.task_dto import TaskDTO, task_to_dto, tasks_to_dto
from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority, TaskStatus


def test_task_to_dto_converts_task_to_task_dto() -> None:
    task = Task(
        title="Buy milk",
        description="After work",
        priority=TaskPriority.HIGH,
    )

    dto = task_to_dto(task)

    assert isinstance(dto, TaskDTO)
    assert dto.id == task.id
    assert dto.title == "Buy milk"
    assert dto.description == "After work"
    assert dto.status == TaskStatus.ACTIVE.value
    assert dto.priority == TaskPriority.HIGH.value
    assert dto.created_at == task.created_at
    assert dto.updated_at == task.updated_at
    assert dto.completed_at == task.completed_at


def test_task_to_dto_returns_plain_strings_for_status_and_priority() -> None:
    task = Task(
        title="Buy milk",
        priority=TaskPriority.HIGH,
    )

    dto = task_to_dto(task)

    assert type(dto.status) is str
    assert type(dto.priority) is str


def test_task_to_dto_converts_completed_task() -> None:
    task = Task(title="Buy milk")
    task.complete()

    dto = task_to_dto(task)

    assert dto.status == TaskStatus.DONE.value
    assert dto.completed_at == task.completed_at


def test_task_to_dto_converts_cancelled_task() -> None:
    task = Task(title="Buy milk")
    task.cancel()

    dto = task_to_dto(task)

    assert dto.status == TaskStatus.CANCELLED.value
    assert dto.completed_at is None


def test_tasks_to_dto_converts_task_list() -> None:
    first_task = Task(title="Task 1")
    second_task = Task(title="Task 2")

    dtos = tasks_to_dto([first_task, second_task])

    assert dtos == [
        task_to_dto(first_task),
        task_to_dto(second_task),
    ]


def test_tasks_to_dto_returns_empty_list_for_empty_input() -> None:
    assert tasks_to_dto([]) == []


def test_task_dto_is_immutable() -> None:
    dto = TaskDTO(
        id="task-id",
        title="Buy milk",
        description=None,
        status=TaskStatus.ACTIVE.value,
        priority=TaskPriority.MEDIUM.value,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        completed_at=None,
    )

    with pytest.raises(FrozenInstanceError):
        dto.title = "New title"
