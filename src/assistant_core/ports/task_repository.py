from abc import ABC, abstractmethod

from assistant_core.domain.entities.task import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task | None:
        pass

    @abstractmethod
    def get_list_all(self) -> list[Task]:
        pass

    @abstractmethod
    def get_list_active(self) -> list[Task]:
        pass

    @abstractmethod
    def delete_by_id(self, task_id: str) -> Task | None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass