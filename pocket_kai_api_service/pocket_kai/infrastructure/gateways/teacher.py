from sqlalchemy import func, insert, or_, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from pocket_kai.application.interfaces.entities.teacher import (
    TeacherReader,
    TeacherSaver,
)
from pocket_kai.domain.entitites.teacher import TeacherEntity
from pocket_kai.domain.exceptions.teacher import TeacherAlreadyExistsError
from pocket_kai.infrastructure.database.models.kai import TeacherModel


class TeacherGateway(TeacherReader, TeacherSaver):
    def __init__(self, session: AsyncSession, search_similarity_threshold: float):
        self._session = session
        self._search_similarity_threshold = search_similarity_threshold

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

    async def suggest_by_name(self, name: str, limit: int) -> list[TeacherEntity]:
        name = name.replace('ё', 'е').lower()

        name_parts_subq = select(
            TeacherModel.id,
            func.unnest(func.string_to_array(func.lower(TeacherModel.name), ' ')).label(
                'name_part',
            ),
        ).cte('name_parts')
        search_query_subq = select(
            func.unnest(func.string_to_array(name.lower(), ' ')).label('query_part'),
        ).cte('search_query')
        similarities_subq = (
            select(
                TeacherModel,
                func.avg(
                    func.similarity(
                        search_query_subq.c.query_part,
                        name_parts_subq.c.name_part,
                    ),
                ).label('avg_similarity'),
            )
            .join(name_parts_subq, TeacherModel.id == name_parts_subq.c.id)
            .join(search_query_subq, text('True'))
            .group_by(TeacherModel.id, TeacherModel.name)
            .cte('similarities')
        )

        similarities_alias = aliased(TeacherModel, similarities_subq)

        stmt = (
            select(similarities_alias)
            .where(
                or_(
                    similarities_subq.c.avg_similarity
                    >= self._search_similarity_threshold,
                    similarities_subq.c.name.ilike(f'%{name}%'),
                ),
            )
            .order_by(
                similarities_subq.c.avg_similarity.desc(),
                similarities_subq.c.name,
            )
            .limit(limit)
        )

        records = await self._session.scalars(stmt)
        return [self._db_to_entity(teacher_record) for teacher_record in records]

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
