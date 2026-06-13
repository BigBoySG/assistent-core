import pytest

from assistant_core.application.services.task_service import TaskService
from assistant_core.composition.factory import create_assistant_core
from assistant_core.infrastructure.persistence.memory.memory_task_repository import (
    MemoryTaskRepository,
)

try:
    from assistant_core.application.api.tasks_api import TasksApi
except ImportError:
    from assistant_core.application.api.tasks_api import TaskApi as TasksApi


@pytest.fixture
def task_repository() -> MemoryTaskRepository:
    return MemoryTaskRepository()


@pytest.fixture
def task_service(task_repository: MemoryTaskRepository) -> TaskService:
    return TaskService(task_repository=task_repository)


@pytest.fixture
def task_api(task_service: TaskService) -> TasksApi:
    return TasksApi(task_service)


@pytest.fixture
def core():
    return create_assistant_core()
