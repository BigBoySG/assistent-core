import pytest

from assistant_core.application.services.task_service import TaskService
from assistant_core.domain.enums import TaskPriority, TaskStatus
from assistant_core.exceptions import InvalidTaskOperationError, TaskNotFoundError
from assistant_core.infrastructure.persistence.memory.memory_task_repository import (
    MemoryTaskRepository,
)


@pytest.fixture
def service() -> TaskService:
    repository = MemoryTaskRepository()
    return TaskService(task_repository=repository)


def test_create_task(service: TaskService):
    task = service.create_task("Купить батарейки")

    assert task.title == "Купить батарейки"
    assert task.description is None
    assert task.status == TaskStatus.ACTIVE
    assert task.priority == TaskPriority.MEDIUM.value
    assert task.completed_at is None


def test_create_task_strips_title(service: TaskService):
    task = service.create_task("  Купить батарейки  ")

    assert task.title == "Купить батарейки"


def test_create_task_with_description_and_priority(service: TaskService):
    task = service.create_task(
        title="Купить батарейки",
        description="Для робота",
        priority=TaskPriority.HIGH,
    )

    assert task.title == "Купить батарейки"
    assert task.description == "Для робота"
    assert task.priority == TaskPriority.HIGH.value


def test_create_task_with_empty_title_raises_error(service: TaskService):
    with pytest.raises(InvalidTaskOperationError):
        service.create_task("   ")


def test_get_task_returns_existing_task(service: TaskService):
    created_task = service.create_task("Купить батарейки")

    found_task = service.get_task(created_task.id)

    assert found_task == created_task


def test_get_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.get_task("unknown-id")


def test_get_all_tasks_returns_all_tasks(service: TaskService):
    first_task = service.create_task("Задача 1")
    second_task = service.create_task("Задача 2")

    tasks = service.get_all_tasks()

    assert tasks == [first_task, second_task]


def test_get_active_tasks_returns_only_active_tasks(service: TaskService):
    active_task = service.create_task("Активная задача")
    done_task = service.create_task("Завершённая задача")
    cancelled_task = service.create_task("Отменённая задача")

    service.complete_task(done_task.id)
    service.cancel_task(cancelled_task.id)

    active_tasks = service.get_active_tasks()

    assert active_tasks == [active_task]


def test_delete_task_returns_deleted_task_and_removes_it(service: TaskService):
    task = service.create_task("Купить батарейки")

    deleted_task = service.delete_task(task.id)

    assert deleted_task == task
    with pytest.raises(TaskNotFoundError):
        service.get_task(task.id)


def test_delete_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.delete_task("unknown-id")


def test_delete_all_tasks_removes_all_tasks(service: TaskService):
    service.create_task("Задача 1")
    service.create_task("Задача 2")

    service.delete_all_tasks()

    assert service.get_all_tasks() == []


def test_complete_active_task_marks_done_and_sets_completed_at(service: TaskService):
    task = service.create_task("Купить батарейки")

    completed_task = service.complete_task(task.id)

    assert completed_task.status == TaskStatus.DONE
    assert completed_task.completed_at is not None


def test_complete_done_task_is_idempotent(service: TaskService):
    task = service.create_task("Купить батарейки")
    completed_task = service.complete_task(task.id)
    completed_at = completed_task.completed_at

    completed_again_task = service.complete_task(task.id)

    assert completed_again_task.status == TaskStatus.DONE
    assert completed_again_task.completed_at == completed_at


def test_complete_cancelled_task_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.complete_task(task.id)


def test_complete_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.complete_task("unknown-id")


def test_reopen_active_task_keeps_active_and_completed_at_none(service: TaskService):
    task = service.create_task("Купить батарейки")

    reopened_task = service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_reopen_done_task_makes_active_and_clears_completed_at(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.complete_task(task.id)

    reopened_task = service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_reopen_cancelled_task_makes_active(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.cancel_task(task.id)

    reopened_task = service.reopen_task(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE
    assert reopened_task.completed_at is None


def test_reopen_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.reopen_task("unknown-id")


def test_cancel_active_task_marks_cancelled(service: TaskService):
    task = service.create_task("Купить батарейки")

    cancelled_task = service.cancel_task(task.id)

    assert cancelled_task.status == TaskStatus.CANCELLED
    assert cancelled_task.completed_at is None


def test_cancel_cancelled_task_is_idempotent(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.cancel_task(task.id)

    cancelled_again_task = service.cancel_task(task.id)

    assert cancelled_again_task.status == TaskStatus.CANCELLED
    assert cancelled_again_task.completed_at is None


def test_cancel_completed_task_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.cancel_task(task.id)


def test_cancel_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.cancel_task("unknown-id")


def test_rename_active_task_changes_title_and_strips_spaces(service: TaskService):
    task = service.create_task("Старое название")

    renamed_task = service.rename_task(task.id, "  Новое название  ")

    assert renamed_task.title == "Новое название"


def test_rename_task_with_empty_title_raises_error(service: TaskService):
    task = service.create_task("Старое название")

    with pytest.raises(InvalidTaskOperationError):
        service.rename_task(task.id, "   ")


def test_rename_done_task_raises_error(service: TaskService):
    task = service.create_task("Старое название")
    service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.rename_task(task.id, "Новое название")


def test_rename_cancelled_task_raises_error(service: TaskService):
    task = service.create_task("Старое название")
    service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.rename_task(task.id, "Новое название")


def test_rename_unknown_task_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.rename_task("unknown-id", "Новое название")


def test_change_task_description_sets_description_and_strips_spaces(service: TaskService):
    task = service.create_task("Купить батарейки")

    changed_task = service.change_task_description(task.id, "  Для робота  ")

    assert changed_task.description == "Для робота"


def test_change_task_description_to_empty_string_clears_description(service: TaskService):
    task = service.create_task("Купить батарейки", description="Для робота")

    changed_task = service.change_task_description(task.id, "   ")

    assert changed_task.description is None


def test_change_task_description_to_none_clears_description(service: TaskService):
    task = service.create_task("Купить батарейки", description="Для робота")

    changed_task = service.change_task_description(task.id, None)

    assert changed_task.description is None


def test_change_done_task_description_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.change_task_description(task.id, "Новое описание")


def test_change_cancelled_task_description_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.change_task_description(task.id, "Новое описание")


def test_change_unknown_task_description_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.change_task_description("unknown-id", "Новое описание")


def test_change_task_priority(service: TaskService):
    task = service.create_task("Купить батарейки")

    changed_task = service.change_task_priority(task.id, TaskPriority.HIGH)

    assert changed_task.priority == TaskPriority.HIGH.value


def test_change_task_priority_to_invalid_value_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")

    with pytest.raises(InvalidTaskOperationError):
        service.change_task_priority(task.id, "high")


def test_change_done_task_priority_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.complete_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.change_task_priority(task.id, TaskPriority.HIGH.value)


def test_change_cancelled_task_priority_raises_error(service: TaskService):
    task = service.create_task("Купить батарейки")
    service.cancel_task(task.id)

    with pytest.raises(InvalidTaskOperationError):
        service.change_task_priority(task.id, TaskPriority.HIGH.value)


def test_change_unknown_task_priority_raises_error(service: TaskService):
    with pytest.raises(TaskNotFoundError):
        service.change_task_priority("unknown-id", TaskPriority.HIGH.value)
