from assistant_core.domain.enums import TaskPriority, TaskStatus


def test_task_api_creates_task(task_api):
    task = task_api.create(
        title="Buy milk",
        description="After work",
        priority=TaskPriority.HIGH,
    )

    assert task.title == "Buy milk"
    assert task.description == "After work"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.ACTIVE


def test_task_api_gets_task_by_id(task_api):
    task = task_api.create("Buy milk")

    found_task = task_api.get(task.id)

    assert found_task == task


def test_task_api_lists_tasks(task_api):
    task_1 = task_api.create("Task 1")
    task_2 = task_api.create("Task 2")

    tasks = task_api.list()

    assert task_1 in tasks
    assert task_2 in tasks
    assert len(tasks) == 2


def test_task_api_returns_active_tasks(task_api):
    active_task = task_api.create("Active task")
    completed_task = task_api.create("Completed task")
    cancelled_task = task_api.create("Cancelled task")
    task_api.complete(completed_task.id)
    task_api.cancel(cancelled_task.id)

    active_tasks = task_api.active()

    assert active_task in active_tasks
    assert completed_task not in active_tasks
    assert cancelled_task not in active_tasks


def test_task_api_deletes_task(task_api):
    task = task_api.create("Buy milk")

    deleted_task = task_api.delete(task.id)

    assert deleted_task == task
    assert task_api.list() == []


def test_task_api_clears_tasks(task_api):
    task_api.create("Task 1")
    task_api.create("Task 2")

    task_api.clear()

    assert task_api.list() == []


def test_task_api_completes_task(task_api):
    task = task_api.create("Buy milk")

    completed_task = task_api.complete(task.id)

    assert completed_task.status == TaskStatus.DONE


def test_task_api_reopens_task(task_api):
    task = task_api.create("Buy milk")
    task_api.complete(task.id)

    reopened_task = task_api.reopen(task.id)

    assert reopened_task.status == TaskStatus.ACTIVE


def test_task_api_cancels_task(task_api):
    task = task_api.create("Buy milk")

    cancelled_task = task_api.cancel(task.id)

    assert cancelled_task.status == TaskStatus.CANCELLED


def test_task_api_renames_task(task_api):
    task = task_api.create("Old title")

    renamed_task = task_api.rename(task.id, "New title")

    assert renamed_task.title == "New title"


def test_task_api_changes_description(task_api):
    task = task_api.create("Buy milk")

    changed_task = task_api.change_description(task.id, "After work")

    assert changed_task.description == "After work"


def test_task_api_changes_priority(task_api):
    task = task_api.create("Buy milk")

    changed_task = task_api.change_priority(task.id, TaskPriority.HIGH)

    assert changed_task.priority == TaskPriority.HIGH
