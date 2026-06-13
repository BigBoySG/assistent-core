import pytest

from assistant_core.domain.enums import TaskPriority, TaskStatus
from assistant_core.exceptions import TaskNotFoundError


def test_service_creates_task(task_service):
    task = task_service.create_task(
        title="Buy milk",
        description="After work",
        priority=TaskPriority.HIGH,
    )

    assert task.title == "Buy milk"
    assert task.description == "After work"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.ACTIVE


def test_service_saves_created_task(task_service):
    task = task_service.create_task(title="Buy milk")

    saved_task = task_service.get_task(task.id)

    assert saved_task == task


def test_service_raises_when_task_is_not_found(task_service):
    with pytest.raises(TaskNotFoundError):
        task_service.get_task("missing-id")


def test_service_returns_all_tasks(task_service):
    task_1 = task_service.create_task("Task 1")
    task_2 = task_service.create_task("Task 2")

    tasks = task_service.get_all_tasks()

    assert task_1 in tasks
    assert task_2 in tasks
    assert len(tasks) == 2


def test_service_returns_only_active_tasks(task_service):
    active_task = task_service.create_task("Active task")
    done_task = task_service.create_task("Done task")
    cancelled_task = task_service.create_task("Cancelled task")
    task_service.complete_task(done_task.id)
    task_service.cancel_task(cancelled_task.id)

    active_tasks = task_service.get_active_tasks()

    assert active_task in active_tasks
    assert done_task not in active_tasks
    assert cancelled_task not in active_tasks


def test_service_deletes_task(task_service):
    task = task_service.create_task("Buy milk")

    deleted_task = task_service.delete_task(task.id)

    assert deleted_task == task
    with pytest.raises(TaskNotFoundError):
        task_service.get_task(task.id)


def test_service_raises_when_deleting_missing_task(task_service):
    with pytest.raises(TaskNotFoundError):
        task_service.delete_task("missing-id")


def test_service_deletes_all_tasks(task_service):
    task_service.create_task("Task 1")
    task_service.create_task("Task 2")

    task_service.delete_all_tasks()

    assert task_service.get_all_tasks() == []


def test_service_completes_task(task_service):
    task = task_service.create_task("Buy milk")

    completed_task = task_service.complete_task(task.id)

    assert completed_task.status == TaskStatus.DONE
    assert completed_task.completed_at is not None


def test_service_reopens_task(task_service):
    task = task_service.create_task("Buy milk")
    task_service.complete_task(task.id)

    reopened_task = task_service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_service_cancels_task(task_service):
    task = task_service.create_task("Buy milk")

    cancelled_task = task_service.cancel_task(task.id)

    assert cancelled_task.status == TaskStatus.CANCELLED


def test_service_renames_task(task_service):
    task = task_service.create_task("Old title")

    renamed_task = task_service.rename_task(task.id, "New title")

    assert renamed_task.title == "New title"


def test_service_changes_task_description(task_service):
    task = task_service.create_task("Buy milk")

    changed_task = task_service.change_task_description(task.id, "After work")

    assert changed_task.description == "After work"


def test_service_changes_task_priority(task_service):
    task = task_service.create_task("Buy milk")

    changed_task = task_service.change_task_priority(task.id, TaskPriority.HIGH)

    assert changed_task.priority == TaskPriority.HIGH
