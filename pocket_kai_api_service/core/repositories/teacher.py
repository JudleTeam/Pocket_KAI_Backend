from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select

from core.entities.teacher import TeacherEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import TeacherModel


class TeacherRepositoryBase(GenericRepository[TeacherEntity], ABC):
    entity = TeacherEntity

    @abstractmethod
    async def get_by_login(self, login: str) -> TeacherEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        login: str,
        name: str,
        department_id: UUID,
    ) -> TeacherEntity:
        raise NotImplementedError


class SATeacherRepository(GenericSARepository[TeacherEntity], TeacherRepositoryBase):
    model_cls = TeacherModel

    async def get_by_login(self, login: str) -> TeacherEntity:
        stmt = select(TeacherModel).where(TeacherModel.login == login)
        teacher = await self._session.scalar(stmt)
        if teacher is None:
            raise EntityNotFoundError(entity=TeacherEntity, find_query=login)
        return await self._convert_db_to_entity(teacher)

    async def create(
        self,
        login: str,
        name: str,
        department_id: UUID | None,
    ) -> TeacherEntity:
        new_teacher = TeacherModel(login=login, name=name, department_id=department_id)
        await self._add(new_teacher)
        await self._session.refresh(new_teacher, ['department'])
        return await self._convert_db_to_entity(new_teacher)
