from typing import Type

from core.entities.base import BaseEntity


class CoreError(Exception):
    def __init__(self, message: str | None = None):
        self.message = message

    def __str__(self) -> str:
        return (
            str(self.__class__.__name__) + f': {self.message}' if self.message else ''
        )


class EntityNotFoundError(CoreError):
    def __init__(
        self,
        entity: Type[BaseEntity],
        find_query,
        message: str | None = None,
    ):
        self.entity = entity
        self.find_query = find_query
        super().__init__(message)

    def __str__(self) -> str:
        return (
            f'{self.entity.__name__.replace('Entity', '')}<{self.find_query}> not found'
        )


class BadRelatedEntityError(CoreError):
    pass


class EntityAlreadyExistsError(CoreError):
    def __init__(self, entity: Type[BaseEntity], message: str | None = None):
        self.entity = entity
        super().__init__(message)
