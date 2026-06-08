from assistant_core.domain.entities.task import Task
from assistant_core.domain.enums import TaskStatus
from assistant_core.ports.task_repository import TaskRepository

class MemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get_by_id(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def get_list_all(self) -> list[Task]:
        return list(self._tasks.values())

    def get_list_active(self) -> list[Task]:
        output_tasks = []
        for task in self._tasks.values():
            if task.status == TaskStatus.ACTIVE:
                output_tasks.append(task)
        return output_tasks

    def delete_by_id(self, task_id: str) -> Task | None:
        return self._tasks.pop(task_id, None)

    def delete_all(self) -> None:
        self._tasks.clear()