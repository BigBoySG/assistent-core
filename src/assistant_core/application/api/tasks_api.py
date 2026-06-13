from assistant_core.application.services.task_service import TaskService
from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority


class TasksApi:
    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    def create(
            self,
            title: str,
            description: str | None = None,
            priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Task:
        return (
            self._task_service.create_task(
                title=title,
                description=description,
                priority=priority
            ))

    def get(self, task_id: str) -> Task:
        return self._task_service.get_task(task_id)

    def get_all(self) -> list[Task]:
        return self._task_service.get_all_tasks()

    def get_active(self) -> list[Task]:
        return self._task_service.get_active_tasks()

    def delete(self, task_id: str) -> Task:
        return self._task_service.delete_task(task_id)

    def clear(self) -> None:
        self._task_service.delete_all_tasks()

    def complete(self, task_id: str) -> Task:
        return self._task_service.complete_task(task_id)

    def reopen(self, task_id: str) -> Task:
        return self._task_service.reopen_task(task_id)

    def cancel(self, task_id: str) -> Task:
        return self._task_service.cancel_task(task_id)

    def rename(self, task_id: str, new_title: str) -> Task:
        return self._task_service.rename_task(task_id, new_title)

    def change_description(
            self,
            task_id: str,
            description: str | None = None
    ) -> Task:
        return self._task_service.change_task_description(task_id, description)

    def change_priority(
            self,
            task_id: str,
            priority: TaskPriority
    ) -> Task:
        return self._task_service.change_task_priority(task_id, priority)
