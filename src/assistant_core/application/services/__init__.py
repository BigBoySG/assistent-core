from assistant_core.application.services.task_service import TaskService
from assistant_core.core import AssistantCore
from assistant_core.infrastructure.persistence.memory.memory_task_repository import MemoryTaskRepository

def create_task_repository() -> AssistantCore:
    task_repository = MemoryTaskRepository()
    task_service = TaskService(task_repository)
    return AssistantCore(task_service)