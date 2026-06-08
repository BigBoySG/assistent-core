from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from assistant_core.domain.enums import TaskPriority, TaskStatus
from assistant_core.exceptions import InvalidTaskOperationError


@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid4()))
    description: str | None = None
    status: TaskStatus = TaskStatus.ACTIVE
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.title.strip() == "":
            raise InvalidTaskOperationError("Title cannot be empty")

        self.title = self.title.strip()

        if self.description is not None:
            self.description = self.description.strip() or None

        if not isinstance(self.status, TaskStatus):
            raise InvalidTaskOperationError("Task status must be of type TaskStatus")

        if not isinstance(self.priority, TaskPriority):
            raise InvalidTaskOperationError("Task priority must be of type TaskPriority")

    def _ensure_editable(self) -> None:
        if self.status == TaskStatus.DONE:
            raise InvalidTaskOperationError("Task is already done, task uneditable")
        if self.status == TaskStatus.CANCELLED:
            raise InvalidTaskOperationError("Task is already cancelled, task uneditable")

    def complete(self) -> None:
        if self.status == TaskStatus.CANCELLED:
            raise InvalidTaskOperationError("Task was cancelled")
        if self.status == TaskStatus.DONE:
            return
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now(timezone.utc)

    def reopen(self) -> None:
        self.status = TaskStatus.ACTIVE
        self.completed_at = None

    def cancel(self) -> None:
        if self.status == TaskStatus.DONE:
            raise InvalidTaskOperationError("Cannot cancel completed task")
        self.status = TaskStatus.CANCELLED

    def rename(self, new_name: str) -> None:
        self._ensure_editable()
        if not new_name.strip():
            raise InvalidTaskOperationError("Task name cannot be empty")
        self.title = new_name.strip()

    def change_description(self, new_description: str | None = None) -> None:
        self._ensure_editable()
        if new_description is None:
            self.description = None
            return
        if new_description.strip() == "":
            self.description = None
            return
        self.description = new_description.strip()

    def change_priority(self, new_priority: TaskPriority) -> None:
        self._ensure_editable()
        if not isinstance(new_priority, TaskPriority):
            raise InvalidTaskOperationError("Task priority must be of type TaskPriority")
        self.priority = new_priority
