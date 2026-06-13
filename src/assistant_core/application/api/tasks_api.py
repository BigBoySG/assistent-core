from assistant_core.application.services.task_service import TaskService
from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority


class TaskApi:
    def __init__(self, task_repository: TaskService):
        self._task_repository = task_repository

    def create(self, title: str,
               description: str | None = None,
               priority: TaskPriority = TaskPriority.MEDIUM
               ) -> Task:
        return self._task_repository.create_task(
            title=title,
            description=description,
            priority=priority
        )

    def get(self, task_id: str) -> Task:
        return self._task_repository.get_task(task_id)\

    def list(self) -> list[Task]:
        return self._task_repository.get_all_tasks()

    def active(self) -> list[Task]:
        return self._task_repository.get_active_tasks()

    def delete(self, task_id: str) -> Task:
        return self._task_repository.delete_task(task_id)

    def clear(self):
        self._task_repository.delete_all_tasks()

    def complete(self, task_id: str) -> Task:
        return self._task_repository.complete_task(task_id)

    def reopen(self, task_id: str) -> Task:
        return self._task_repository.reopen_task(task_id)

    def cancel(self, task_id: str) -> Task:
        return self._task_repository.cancel_task(task_id)

    def rename(self, task_id: str, new_title: str) -> Task:
        return self._task_repository.rename_task(task_id, new_title)

    def change_description(self,task_id: str,  description: str | None = None) -> Task:
        return self._task_repository.change_task_description(task_id, description)

    def change_priority(self,task_id: str, priority: TaskPriority) -> Task:
        return self._task_repository.change_task_priority(task_id, priority)
