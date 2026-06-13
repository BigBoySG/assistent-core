from assistant_core import TaskPriority, TaskStatus, create_assistant_core


def test_create_assistant_core_returns_core_with_tasks_api():
    core = create_assistant_core()

    assert hasattr(core, "tasks")


def test_public_core_can_create_task_through_tasks_api():
    core = create_assistant_core()

    task = core.tasks.create(
        title="Buy milk",
        priority=TaskPriority.HIGH,
    )

    assert task.title == "Buy milk"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.ACTIVE


def test_public_core_instances_do_not_share_memory_storage():
    first_core = create_assistant_core()
    second_core = create_assistant_core()

    first_core.tasks.create("Task in first core")

    assert len(first_core.tasks.get_all()) == 1
    assert second_core.tasks.get_all() == []
