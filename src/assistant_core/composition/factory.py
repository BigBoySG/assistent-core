from assistant_core.application.api.tasks_api import TasksApi
from assistant_core.application.services.task_service import TaskService
from assistant_core.core import AssistantCore
from assistant_core.infrastructure.persistence.memory.memory_task_repository import (
    MemoryTaskRepository,
)


def create_assistant_core() -> AssistantCore:
    task_repository = MemoryTaskRepository()
    task_service = TaskService(task_repository=task_repository)
    task_api = TasksApi(task_service=task_service)
    assistant_core = AssistantCore(tasks=task_api)
    return assistant_core