import dataclasses

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pocket_kai.application.dto.exam import ExamExtendedDTO
from pocket_kai.application.interfaces.entities.exam import (
    ExamDeleter,
    ExamReader,
    ExamSaver,
    ExamUpdater,
)
from pocket_kai.domain.entitites.exam import ExamEntity
from pocket_kai.infrastructure.database.models.kai.exam import ExamModel
from pocket_kai.infrastructure.gateways.discipline import DisciplineGateway
from pocket_kai.infrastructure.gateways.teacher import TeacherGateway


class ExamGateway(ExamSaver, ExamReader, ExamDeleter, ExamUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def db_to_entity(exam_record: ExamModel | None) -> ExamEntity | None:
        if exam_record is None:
            return None

        return ExamEntity(
            id=exam_record.id,
            created_at=exam_record.created_at,
            original_date=exam_record.original_date,
            time=exam_record.time,
            audience_number=exam_record.audience_number,
            building_number=exam_record.building_number,
            parsed_date=exam_record.parsed_date,
            academic_year=exam_record.academic_year,
            academic_year_half=exam_record.academic_year_half,
            semester=exam_record.semester,
            discipline_id=exam_record.discipline_id,
            teacher_id=exam_record.teacher_id,
            group_id=exam_record.group_id,
        )

    @staticmethod
    def db_to_extended_dto(exam_record: ExamModel | None) -> ExamExtendedDTO | None:
        if exam_record is None:
            return None

        return ExamExtendedDTO(
            id=exam_record.id,
            created_at=exam_record.created_at,
            original_date=exam_record.original_date,
            time=exam_record.time,
            audience_number=exam_record.audience_number,
            building_number=exam_record.building_number,
            parsed_date=exam_record.parsed_date,
            academic_year=exam_record.academic_year,
            academic_year_half=exam_record.academic_year_half,
            semester=exam_record.semester,
            discipline_id=exam_record.discipline_id,
            teacher_id=exam_record.teacher_id,
            group_id=exam_record.group_id,
            teacher=TeacherGateway._db_to_entity(exam_record.teacher),
            discipline=DisciplineGateway._db_to_entity(exam_record.discipline),
        )

    async def save(self, exam: ExamEntity) -> None:
        await self._session.execute(
            insert(ExamModel).values(**dataclasses.asdict(exam)),
        )

    async def get_by_id(self, exam_id: str) -> ExamEntity:
        exam = await self._session.get(ExamModel, exam_id)
        return self.db_to_entity(exam)

    async def get_by_id_extended(self, exam_id: str) -> ExamExtendedDTO:
        exam = await self._session.get(
            ExamModel,
            exam_id,
            options=[
                selectinload(ExamModel.teacher),
                selectinload(ExamModel.discipline),
            ],
        )
        return self.db_to_extended_dto(exam)

    async def get_by_group_id(
        self,
        group_id: str,
        academic_year: str | None,
        academic_year_half: int | None,
    ) -> list[ExamEntity]:
        stmt = select(ExamModel).where(ExamModel.group_id == group_id)
        if academic_year is not None:
            stmt = stmt.where(ExamModel.academic_year == academic_year)
        if academic_year_half is not None:
            stmt = stmt.where(ExamModel.academic_year_half == academic_year_half)
        exams = await self._session.scalars(stmt)

        return [self.db_to_entity(exam) for exam in exams]

    async def get_by_group_id_extended(
        self,
        group_id: str,
        academic_year: str | None,
        academic_year_half: int | None,
    ) -> list[ExamExtendedDTO]:
        stmt = select(ExamModel).where(ExamModel.group_id == group_id)
        if academic_year is not None:
            stmt = stmt.where(ExamModel.academic_year == academic_year)
        if academic_year_half is not None:
            stmt = stmt.where(ExamModel.academic_year_half == academic_year_half)

        stmt = stmt.options(
            selectinload(ExamModel.teacher),
            selectinload(ExamModel.discipline),
        )

        exams = await self._session.scalars(stmt)

        return [self.db_to_extended_dto(exam) for exam in exams]

    async def delete(self, exam_id: str) -> None:
        await self._session.execute(
            delete(ExamModel).where(ExamModel.id == exam_id),
        )

    async def update(self, exam: ExamEntity) -> None:
        await self._session.execute(
            update(ExamModel)
            .where(ExamModel.id == exam.id)
            .values(**dataclasses.asdict(exam)),
        )
