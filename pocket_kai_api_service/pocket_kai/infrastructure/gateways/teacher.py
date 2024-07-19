from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.teacher import (
    TeacherReader,
    TeacherSaver,
)
from pocket_kai.domain.entitites.teacher import TeacherEntity
from pocket_kai.domain.exceptions.teacher import TeacherAlreadyExistsError
from pocket_kai.infrastructure.database.models.kai import TeacherModel


class TeacherGateway(TeacherReader, TeacherSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(teacher_record: TeacherModel | None) -> TeacherEntity | None:
        if teacher_record is None:
            return None

        return TeacherEntity(
            id=teacher_record.id,
            created_at=teacher_record.created_at,
            login=teacher_record.login,
            name=teacher_record.name,
        )

    async def get_by_login(self, login: str) -> TeacherEntity | None:
        teacher_record = await self._session.scalar(
            select(TeacherModel).where(TeacherModel.login == login),
        )

        return self._db_to_entity(teacher_record)

    async def get_by_id(self, id: str) -> TeacherEntity | None:
        teacher_record = await self._session.scalar(
            select(TeacherModel).where(TeacherModel.id == id),
        )

        return self._db_to_entity(teacher_record)

    async def save(self, teacher: TeacherEntity) -> None:
        try:
            await self._session.execute(
                insert(TeacherModel).values(
                    id=teacher.id,
                    created_at=teacher.created_at,
                    login=teacher.login,
                    name=teacher.name,
                ),
            )
        except IntegrityError:
            raise TeacherAlreadyExistsError
