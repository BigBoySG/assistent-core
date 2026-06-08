class AssistantCoreError(Exception):
    """Base exception for assistant core."""


class TaskNotFoundError(AssistantCoreError):
    """Raised when task is not found."""


class InvalidTaskOperationError(AssistantCoreError):
    """Raised when task operation is not allowed."""