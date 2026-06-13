from assistant_core import TaskStatus


def test_public_core_can_complete_task_through_tasks_api(core) -> None:
    task = core.tasks.create("Buy milk")

    completed_task = core.tasks.complete(task.id)

    assert completed_task.status == TaskStatus.DONE
    assert completed_task.completed_at is not None
    assert completed_task in core.tasks.get_list()
