from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority
from assistant_core.exceptions import TaskNotFoundError
from assistant_core.ports.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def create_task(self,
                    title: str,
                    description: str | None = None,
                    priority: TaskPriority = TaskPriority.MEDIUM) -> Task:

        task = Task(
            title=title,
            description=description,
            priority=priority
        )

        self._task_repository.save(task)

        return task

    def get_task(self, task_id: str) -> Task:
        task = self._task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        return task

    def get_all_tasks(self) -> list[Task]:
        return self._task_repository.get_list_all()

    def get_active_tasks(self) -> list[Task]:
        return self._task_repository.get_list_active()

    def delete_task(self, task_id: str) -> Task:
        task = self._task_repository.delete_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        return task

    def delete_all_tasks(self) -> None:
        self._task_repository.delete_all()

    def complete_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)

        task.complete()
        self._task_repository.save(task)

        return task

    def reopen_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)

        task.reopen()
        self._task_repository.save(task)

        return task

    def cancel_task(self, task_id: str) -> Task:
        task = self.get_task(task_id)

        task.cancel()
        self._task_repository.save(task)

        return task

    def rename_task(self, task_id: str, new_title: str) -> Task:
        task = self.get_task(task_id)

        task.rename(new_title)
        self._task_repository.save(task)

        return task

    def change_task_description(self, task_id: str, new_description: str | None = None) -> Task:
        task = self.get_task(task_id)

        task.change_description(new_description)
        self._task_repository.save(task)

        return task

    def change_task_priority(self, task_id: str, new_priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        task = self.get_task(task_id)

        task.change_priority(new_priority)
        self._task_repository.save(task)

        return task

