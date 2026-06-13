from assistant_core.application.api.tasks_api import TaskApi

class AssistantCore:
    def __init__(self, tasks: TaskApi) -> None:
        self.tasks = tasks
