from dataclasses import dataclass
from datetime import datetime

from assistant_core.domain.entities.task import Task


@dataclass(frozen=True)
class TaskDTO:
    id: str
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None


def task_to_dto(task: Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
    )


def tasks_to_dto(tasks: list[Task]) -> list[TaskDTO]:
    return [task_to_dto(task) for task in tasks]
