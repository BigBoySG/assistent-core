from assistant_core.application.services.task_service import TaskService
from assistant_core.core import AssistantCore
from assistant_core.infrastructure.persistence.memory.memory_task_repository import (
    MemoryTaskRepository,
)


def create_assistant_core() -> AssistantCore:
    task_repository = MemoryTaskRepository()

    task_service = TaskService(
        task_repository=task_repository,
    )

    assistant_core = AssistantCore(
        task_service=task_service,
    )

    return assistant_core