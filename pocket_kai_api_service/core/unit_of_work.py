from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session


class UnitOfWorkBase(ABC):
    """
    Unit of work.
    """

    @abstractmethod
    async def commit(self):
        """
        Commits the current transaction.
        """
        raise NotImplementedError()

    @abstractmethod
    async def flush(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        """
        Rollbacks the current transaction.
        """
        raise NotImplementedError()


class SAUnitOfWork(UnitOfWorkBase):
    def __init__(self, session: AsyncSession):
        """
        Creates a new uow instance.
        """
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def flush(self):
        await self._session.flush()


def get_uow(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UnitOfWorkBase:
    return SAUnitOfWork(session)
