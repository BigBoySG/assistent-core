import pytest

from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority, TaskStatus
from assistant_core.exceptions import InvalidTaskOperationError


def test_task_is_created_with_default_values():
    task = Task(title="Buy milk")

    assert task.title == "Buy milk"
    assert task.description is None
    assert task.status == TaskStatus.ACTIVE
    assert task.priority == TaskPriority.MEDIUM
    assert task.completed_at is None
    assert task.id
    assert task.created_at is not None


def test_task_strips_title_and_description():
    task = Task(title="  Buy milk  ", description="  After work  ")

    assert task.title == "Buy milk"
    assert task.description == "After work"


@pytest.mark.parametrize("title", ["", "   "])
def test_task_cannot_be_created_with_empty_title(title: str):
    with pytest.raises(InvalidTaskOperationError):
        Task(title=title)


def test_empty_description_becomes_none():
    task = Task(title="Buy milk", description="   ")

    assert task.description is None


def test_task_complete_changes_status_and_sets_completed_at():
    task = Task(title="Buy milk")

    task.complete()

    assert task.status == TaskStatus.DONE
    assert task.completed_at is not None


def test_complete_done_task_is_idempotent():
    task = Task(title="Buy milk")
    task.complete()
    completed_at = task.completed_at

    task.complete()

    assert task.status == TaskStatus.DONE
    assert task.completed_at == completed_at


def test_task_reopen_makes_task_active_and_clears_completed_at():
    task = Task(title="Buy milk")
    task.complete()

    task.reopen()

    assert task.status == TaskStatus.ACTIVE
    assert task.completed_at is None


def test_task_cancel_changes_status_to_cancelled():
    task = Task(title="Buy milk")

    task.cancel()

    assert task.status == TaskStatus.CANCELLED


def test_cancel_completed_task_is_not_allowed():
    task = Task(title="Buy milk")
    task.complete()

    with pytest.raises(InvalidTaskOperationError):
        task.cancel()


def test_complete_cancelled_task_is_not_allowed():
    task = Task(title="Buy milk")
    task.cancel()

    with pytest.raises(InvalidTaskOperationError):
        task.complete()


def test_task_can_be_renamed():
    task = Task(title="Old title")

    task.rename("  New title  ")

    assert task.title == "New title"


@pytest.mark.parametrize("new_title", ["", "   "])
def test_task_cannot_be_renamed_to_empty_title(new_title: str):
    task = Task(title="Old title")

    with pytest.raises(InvalidTaskOperationError):
        task.rename(new_title)


def test_completed_task_cannot_be_renamed():
    task = Task(title="Old title")
    task.complete()

    with pytest.raises(InvalidTaskOperationError):
        task.rename("New title")


def test_cancelled_task_cannot_be_renamed():
    task = Task(title="Old title")
    task.cancel()

    with pytest.raises(InvalidTaskOperationError):
        task.rename("New title")


def test_task_description_can_be_changed():
    task = Task(title="Buy milk")

    task.change_description("  After work  ")

    assert task.description == "After work"


@pytest.mark.parametrize("description", [None, "", "   "])
def test_task_description_can_be_cleared(description: str | None):
    task = Task(title="Buy milk", description="After work")

    task.change_description(description)

    assert task.description is None


def test_completed_task_description_cannot_be_changed():
    task = Task(title="Buy milk")
    task.complete()

    with pytest.raises(InvalidTaskOperationError):
        task.change_description("New description")


def test_task_priority_can_be_changed():
    task = Task(title="Buy milk")

    task.change_priority(TaskPriority.HIGH)

    assert task.priority == TaskPriority.HIGH


def test_task_priority_must_be_task_priority_enum():
    task = Task(title="Buy milk")

    with pytest.raises(InvalidTaskOperationError):
        task.change_priority("high")
