from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.dto.discipline import (
    DisciplineTypeWithTeacherDTO,
    DisciplineWithTypesDTO,
)
from pocket_kai.application.interfaces.entities.discipline import (
    DisciplineReader,
    DisciplineSaver,
)
from pocket_kai.domain.entitites.discipline import DisciplineEntity
from pocket_kai.domain.entitites.teacher import TeacherEntity
from pocket_kai.infrastructure.database.models.kai import (
    DisciplineModel,
    LessonModel,
    TeacherModel,
)


class DisciplineGateway(DisciplineReader, DisciplineSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(
        discipline_record: DisciplineModel | None,
    ) -> DisciplineEntity | None:
        if not discipline_record:
            return None

        return DisciplineEntity(
            id=discipline_record.id,
            created_at=discipline_record.created_at,
            kai_id=discipline_record.kai_id,
            name=discipline_record.name,
        )

    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(DisciplineModel).where(DisciplineModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> DisciplineEntity | None:
        return self._db_to_entity(
            await self._session.get(DisciplineModel, id),
        )

    async def get_by_group_id_with_teachers(
        self,
        group_id: str,
    ) -> list[DisciplineWithTypesDTO]:
        stmt = (
            select(
                DisciplineModel.id.label('discipline_id'),
                DisciplineModel.kai_id.label('discipline_kai_id'),
                DisciplineModel.name.label('discipline_name'),
                TeacherModel.login.label('teacher_login'),
                TeacherModel.name.label('teacher_name'),
                TeacherModel.id.label('teacher_id'),
                TeacherModel.created_at.label('teacher_created_at'),
                LessonModel.parsed_lesson_type.label('parsed_lesson_type'),
                LessonModel.original_lesson_type.label('original_lesson_type'),
            )
            .join(
                LessonModel,
                LessonModel.discipline_id == DisciplineModel.id,
            )
            .outerjoin(
                TeacherModel,
                TeacherModel.id == LessonModel.teacher_id,
            )
            .group_by(
                DisciplineModel,
                TeacherModel,
                LessonModel.parsed_lesson_type,
                LessonModel.original_lesson_type,
            )
            .where(
                LessonModel.group_id == group_id,
            )
            .order_by(
                DisciplineModel.name,
                LessonModel.parsed_lesson_type,
            )
        )

        result_rows = await self._session.execute(stmt)

        # Сохраняется порядок из результирующего набора
        disciplines = dict()
        for row in result_rows:
            discipline_type = DisciplineTypeWithTeacherDTO(
                parsed_type=row.parsed_lesson_type,
                original_type=row.original_lesson_type,
                teacher=TeacherEntity(
                    id=row.teacher_id,
                    created_at=row.teacher_created_at,
                    login=row.teacher_login,
                    name=row.teacher_name,
                )
                if row.teacher_id
                else None,
            )

            if row.discipline_kai_id not in disciplines:
                disciplines[row.discipline_kai_id] = DisciplineWithTypesDTO(
                    id=row.discipline_id,
                    kai_id=row.discipline_kai_id,
                    name=row.discipline_name,
                    types=[discipline_type],
                )
            else:
                disciplines[row.discipline_kai_id].types.append(discipline_type)

        return list(disciplines.values())

    async def save(self, discipline: DisciplineEntity) -> None:
        await self._session.execute(
            insert(DisciplineModel).values(
                id=discipline.id,
                created_at=discipline.created_at,
                kai_id=discipline.kai_id,
                name=discipline.name,
            ),
        )
