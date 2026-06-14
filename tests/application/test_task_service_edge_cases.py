import pytest

from assistant_core.domain.enums import TaskPriority, TaskStatus
from assistant_core.exceptions import InvalidTaskOperationError, TaskNotFoundError


def test_service_create_task_strips_title(task_service) -> None:
    task = task_service.create_task("  Buy milk  ")

    assert task.title == "Buy milk"


def test_service_create_task_with_empty_title_raises_error(task_service) -> None:
    with pytest.raises(InvalidTaskOperationError):
        task_service.create_task("   ")


def test_service_get_all_tasks_preserves_creation_order(task_service) -> None:
    first_task = task_service.create_task("Task 1")
    second_task = task_service.create_task("Task 2")

    tasks = task_service.get_all_tasks()

    assert tasks == [first_task, second_task]


def test_service_get_active_tasks_returns_only_active_tasks_in_order(task_service) -> None:
    active_task = task_service.create_task("Active task")
    done_task = task_service.create_task("Done task")
    cancelled_task = task_service.create_task("Cancelled task")

    task_service.complete_task(done_task.id)
    task_service.cancel_task(cancelled_task.id)

    active_tasks = task_service.get_active_tasks()

    assert active_tasks == [active_task]


def test_service_complete_done_task_is_idempotent(task_service) -> None:
    task = task_service.create_task("Buy milk")
    completed_task = task_service.complete_task(task.id)
    completed_at = completed_task.completed_at

    completed_again_task = task_service.complete_task(task.id)

    assert completed_again_task.status == TaskStatus.DONE
    assert completed_again_task.completed_at == completed_at


def test_service_complete_cancelled_task_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.complete_task(task.id)


def test_service_complete_unknown_task_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.complete_task("unknown-id")


def test_service_reopen_active_task_keeps_active_and_completed_at_none(task_service) -> None:
    task = task_service.create_task("Buy milk")

    reopened_task = task_service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_service_reopen_cancelled_task_makes_active(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.cancel_task(task.id)

    reopened_task = task_service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_service_reopen_unknown_task_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.reopen_task("unknown-id")


def test_service_cancel_cancelled_task_is_idempotent(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.cancel_task(task.id)

    cancelled_again_task = task_service.cancel_task(task.id)

    assert cancelled_again_task.status == TaskStatus.CANCELLED
    assert cancelled_again_task.completed_at is None


def test_service_cancel_completed_task_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.cancel_task(task.id)


def test_service_cancel_unknown_task_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.cancel_task("unknown-id")


def test_service_rename_task_strips_spaces(task_service) -> None:
    task = task_service.create_task("Old title")

    renamed_task = task_service.rename_task(task.id, "  New title  ")

    assert renamed_task.title == "New title"


def test_service_rename_task_with_empty_title_raises_error(task_service) -> None:
    task = task_service.create_task("Old title")

    with pytest.raises(InvalidTaskOperationError):
        task_service.rename_task(task.id, "   ")


def test_service_rename_done_task_raises_error(task_service) -> None:
    task = task_service.create_task("Old title")
    task_service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.rename_task(task.id, "New title")


def test_service_rename_cancelled_task_raises_error(task_service) -> None:
    task = task_service.create_task("Old title")
    task_service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.rename_task(task.id, "New title")


def test_service_rename_unknown_task_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.rename_task("unknown-id", "New title")


def test_service_change_task_description_strips_spaces(task_service) -> None:
    task = task_service.create_task("Buy milk")

    changed_task = task_service.change_task_description(task.id, "  After work  ")

    assert changed_task.description == "After work"


@pytest.mark.parametrize("description", [None, "", "   "])
def test_service_change_task_description_can_clear_description(
    task_service,
    description: str | None,
) -> None:
    task = task_service.create_task("Buy milk", description="After work")

    changed_task = task_service.change_task_description(task.id, description)

    assert changed_task.description is None


def test_service_change_done_task_description_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.change_task_description(task.id, "New description")


def test_service_change_cancelled_task_description_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.change_task_description(task.id, "New description")


def test_service_change_unknown_task_description_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.change_task_description("unknown-id", "New description")


def test_service_change_task_priority_to_invalid_value_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")

    with pytest.raises(InvalidTaskOperationError):
        task_service.change_task_priority(task.id, "high")


def test_service_change_done_task_priority_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.change_task_priority(task.id, TaskPriority.HIGH)


def test_service_change_cancelled_task_priority_raises_error(task_service) -> None:
    task = task_service.create_task("Buy milk")
    task_service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        task_service.change_task_priority(task.id, TaskPriority.HIGH)


def test_service_change_unknown_task_priority_raises_error(task_service) -> None:
    with pytest.raises(TaskNotFoundError):
        task_service.change_task_priority("unknown-id", TaskPriority.HIGH)
