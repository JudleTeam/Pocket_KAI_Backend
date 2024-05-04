from abc import ABC, abstractmethod
from typing import Type
from uuid import UUID

from sqlalchemy import select, and_, Select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.entities.base import BaseEntity
from core.exceptions.base import (
    BadRelatedEntityError,
    EntityNotFoundError,
    EntityAlreadyExistsError,
)
from database.base import Base


class GenericRepository[T: BaseEntity](ABC):
    entity: Type[T]

    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None:
        """
        Get a single record by id

        :param id: Record id
        :return: Record or None
        """
        raise NotImplementedError()

    @abstractmethod
    async def list(self, offset: int = 0, limit: int = 100, **filters) -> list[T]:
        """
        Get a list of records

        :param limit:
        :param offset:
        :param filters: Filter conditions, several criteria are linked with a logical 'and'
        :raise ValueError: Invalid filter condition
        :return: List of records
        """
        raise NotImplementedError()

    @abstractmethod
    async def add(self, entity: T) -> T:
        """
        Creates a new record

        :param entity: The record to be created
        :return: The created record
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, entity: T, **kwargs) -> T:
        """
        Updates an existing record.
        Searches for the record needed to update by the id attribute in the transferred record

        :param entity: The record to be updated including record id
        :return: The updated record
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """
        Deletes a record by id

        :param id: Record id
        :return: None
        """
        raise NotImplementedError()


class GenericSARepository[T: BaseEntity](GenericRepository[T], ABC):
    model_cls: Type[Base]

    def __init__(self, session: AsyncSession) -> None:
        """
        Creates a new repository instance

        :param session: SQLAlchemy async session
        """
        self._session = session

    async def _convert_db_to_entity(self, record: Base, **kwargs) -> T:
        return self.entity.model_validate(record)

    async def _convert_entity_to_db(self, entity: T, **kwargs) -> Base:
        return self.model_cls(**entity.model_dump())

    async def _convert_entity_to_update_dict(self, entity: T, **kwargs) -> dict:
        return entity.model_dump(exclude={'id'})

    def _construct_get_stmt(self, id: UUID) -> Select:
        """
        Creates a SELECT query for retrieving a single record

        :param id: Record id
        :return: SELECT statement
        """
        stmt = select(self.model_cls).where(self.model_cls.id == id)

        return stmt

    def _construct_list_stmt(self, offset, limit, **filters) -> Select:
        """
        Creates a SELECT query for retrieving a multiple records

        :param offset:
        :param limit:
        :param filters: Filter conditions, several criteria are linked with a logical 'and'
        :return: SELECT statement
        """
        stmt = select(self.model_cls)
        where_clauses = []
        for column, value in filters.items():
            if not hasattr(self.model_cls, column):
                raise ValueError(f'Invalid column name {column}')
            where_clauses.append(getattr(self.model_cls, column) == value)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))

        stmt = stmt.offset(offset).limit(limit)

        return stmt

    async def get_by_id(self, id: UUID, **kwargs) -> T | None:
        stmt = self._construct_get_stmt(id)
        result = await self._session.scalar(stmt)

        if result is None:
            raise EntityNotFoundError(entity=self.entity, find_query=id)

        return await self._convert_db_to_entity(result, **kwargs)

    async def list(
        self, offset=0, limit=100, filters: dict = None, **kwargs
    ) -> list[T]:
        if filters is None:
            filters = {}

        stmt = self._construct_list_stmt(offset=offset, limit=limit, **filters)
        records = await self._session.scalars(stmt)

        return [
            await self._convert_db_to_entity(record, **kwargs)
            for record in records.all()
        ]

    async def add(self, entity: T, **kwargs) -> T:
        record = await self._convert_entity_to_db(entity)

        self._session.add(record)

        try:
            await self._session.flush()
        except IntegrityError as error:
            if 'ForeignKeyViolationError' in str(error):
                raise BadRelatedEntityError from error
            if 'UniqueViolationError' in str(error):
                raise EntityAlreadyExistsError(entity=self.entity) from error

            raise error

        await self._session.refresh(record)

        return await self._convert_db_to_entity(record, **kwargs)

    async def update(self, entity: T, **kwargs) -> T:
        stmt = (
            update(self.model_cls)
            .where(self.model_cls.id == entity.id)
            .values(**await self._convert_entity_to_update_dict(entity, **kwargs))
            .returning(self.model_cls)
        )

        try:
            record = await self._session.scalar(stmt)
        except IntegrityError as error:
            if 'ForeignKeyViolationError' in str(error):
                raise BadRelatedEntityError from error
            raise error

        if record is None:
            raise EntityNotFoundError(entity=self.entity, find_query=entity.id)

        return await self._convert_db_to_entity(record, **kwargs)

    async def delete(self, id: UUID) -> None:
        stmt = delete(self.model_cls).where(self.model_cls.id == id)

        await self._session.execute(stmt)
