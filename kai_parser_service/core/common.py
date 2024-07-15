from enum import Enum


class TaskType(str, Enum):
    """Task type enum."""

    GROUP_MEMBERS = 'group_members'
    GROUP_DOCUMENTS = 'group_documents'


class TaskStatus(str, Enum):
    """Task status enum."""

    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
