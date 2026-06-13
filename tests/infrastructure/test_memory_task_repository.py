from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskStatus


def test_repository_saves_and_gets_task_by_id(task_repository):
    task = Task(title="Buy milk")

    task_repository.save(task)

    assert task_repository.get_by_id(task.id) == task


def test_repository_returns_none_when_task_does_not_exist(task_repository):
    assert task_repository.get_by_id("missing-id") is None


def test_repository_returns_all_tasks(task_repository):
    task_1 = Task(title="Task 1")
    task_2 = Task(title="Task 2")
    task_repository.save(task_1)
    task_repository.save(task_2)

    tasks = task_repository.get_list_all()

    assert task_1 in tasks
    assert task_2 in tasks
    assert len(tasks) == 2


def test_repository_returns_only_active_tasks(task_repository):
    active_task = Task(title="Active task")
    done_task = Task(title="Done task")
    cancelled_task = Task(title="Cancelled task")
    done_task.complete()
    cancelled_task.cancel()
    task_repository.save(active_task)
    task_repository.save(done_task)
    task_repository.save(cancelled_task)

    active_tasks = task_repository.get_list_active()

    assert active_task in active_tasks
    assert done_task not in active_tasks
    assert cancelled_task not in active_tasks
    assert all(task.status == TaskStatus.ACTIVE for task in active_tasks)


def test_repository_deletes_task_by_id(task_repository):
    task = Task(title="Buy milk")
    task_repository.save(task)

    deleted_task = task_repository.delete_by_id(task.id)

    assert deleted_task == task
    assert task_repository.get_by_id(task.id) is None


def test_repository_returns_none_when_deleting_missing_task(task_repository):
    assert task_repository.delete_by_id("missing-id") is None


def test_repository_deletes_all_tasks(task_repository):
    task_repository.save(Task(title="Task 1"))
    task_repository.save(Task(title="Task 2"))

    task_repository.delete_all()

    assert task_repository.get_list_all() == []
