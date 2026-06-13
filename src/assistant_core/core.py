from assistant_core.application.api.tasks_api import TasksApi

class AssistantCore:
    def __init__(self, tasks: TasksApi) -> None:
        self.tasks = tasks
