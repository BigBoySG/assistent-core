from assistant_core.application.services.task_service import TaskService
from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskPriority

class AssistantCore:
    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    def create_task(self,
                    title: str,
                    description: str | None = None,
                    priority: TaskPriority = TaskPriority.MEDIUM) -> Task:

        return self._task_service.create_task(
            title=title,
            description=description,
            priority=priority,
        )

    def get_task(self, task_id: str) -> Task:
        return self._task_service.get_task(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self._task_service.get_all_tasks()

    def get_active_tasks(self) -> list[Task]:
        return self._task_service.get_active_tasks()

    def delete_all_tasks(self) -> None:
        self._task_service.delete_all_tasks()

    def delete_task(self, task_id: str) -> Task:
        return self._task_service.delete_task(task_id)

    def complete_task(self, task_id: str) -> Task:
        return self._task_service.complete_task(task_id)

    def reopen_task(self, task_id: str) -> Task:
        return self._task_service.reopen_task(task_id)

    def cancel_task(self, task_id: str) -> Task:
        return self._task_service.cancel_task(task_id)

    def rename_task(self, task_id: str, new_title: str) -> Task:
        return self._task_service.rename_task(task_id, new_title)

    def change_task_priority(self, task_id: str, new_priority: TaskPriority) -> Task:
        return self._task_service.change_task_priority(task_id, new_priority)

    def change_task_description(self, task_id: str, new_description: str | None = None) -> Task:
        return self._task_service.change_task_description(task_id, new_description)