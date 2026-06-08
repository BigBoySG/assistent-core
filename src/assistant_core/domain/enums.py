from enum import Enum

class TaskStatus(str, Enum):
    ACTIVE = "active"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"