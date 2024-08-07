from typing import Iterable

import dataclasses

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pocket_kai.application.dto.lesson import (
    LessonExtendedDTO,
    LessonPatchDTO,
    TeacherLessonExtendedDTO,
)
from pocket_kai.application.interfaces.entities.lesson import (
    LessonDeleter,
    LessonReader,
    LessonSaver,
    LessonUpdater,
)
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.entitites.lesson import LessonEntity
from pocket_kai.domain.exceptions.base import BadRelatedEntityError
from pocket_kai.infrastructure.database.models.kai import LessonModel
from pocket_kai.infrastructure.gateways.department import DepartmentGateway
from pocket_kai.infrastructure.gateways.discipline import DisciplineGateway
from pocket_kai.infrastructure.gateways.group import GroupGateway
from pocket_kai.infrastructure.gateways.teacher import TeacherGateway


class LessonGateway(LessonReader, LessonSaver, LessonUpdater, LessonDeleter):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(lesson_record: LessonModel | None) -> LessonEntity | None:
        if lesson_record is None:
            return None

        return LessonEntity(
            id=lesson_record.id,
            created_at=lesson_record.created_at,
            number_of_day=lesson_record.number_of_day,
            original_dates=lesson_record.original_dates,
            parsed_parity=lesson_record.parsed_parity,
            parsed_dates=lesson_record.parsed_dates,
            parsed_dates_status=lesson_record.parsed_dates_status,
            start_time=lesson_record.start_time,
            end_time=lesson_record.end_time,
            audience_number=lesson_record.audience_number,
            building_number=lesson_record.building_number,
            original_lesson_type=lesson_record.original_lesson_type,
            parsed_lesson_type=lesson_record.parsed_lesson_type,
            group_id=lesson_record.group_id,
            discipline_id=lesson_record.discipline_id,
            department_id=lesson_record.department_id,
            teacher_id=lesson_record.teacher_id,
        )

    @staticmethod
    def _db_to_extended_dto(
        lesson_record: LessonModel | None,
    ) -> LessonExtendedDTO | None:
        if lesson_record is None:
            return None

        return LessonExtendedDTO(
            id=lesson_record.id,
            created_at=lesson_record.created_at,
            number_of_day=lesson_record.number_of_day,
            original_dates=lesson_record.original_dates,
            parsed_parity=lesson_record.parsed_parity,
            parsed_dates=lesson_record.parsed_dates,
            parsed_dates_status=lesson_record.parsed_dates_status,
            start_time=lesson_record.start_time,
            end_time=lesson_record.end_time,
            audience_number=lesson_record.audience_number,
            building_number=lesson_record.building_number,
            original_lesson_type=lesson_record.original_lesson_type,
            parsed_lesson_type=lesson_record.parsed_lesson_type,
            group_id=lesson_record.group_id,
            discipline_id=lesson_record.discipline_id,
            department_id=lesson_record.department_id,
            teacher_id=lesson_record.teacher_id,
            teacher=TeacherGateway._db_to_entity(lesson_record.teacher),
            department=DepartmentGateway.db_to_entity(lesson_record.department),
            discipline=DisciplineGateway._db_to_entity(lesson_record.discipline),
        )

    @staticmethod
    def db_to_teacher_extended_dto(
        lesson_records: Iterable[LessonModel],
    ) -> list[TeacherLessonExtendedDTO]:
        result_dict = dict()
        for lesson_record in lesson_records:
            lesson_key = (
                lesson_record.number_of_day,
                lesson_record.start_time,
                lesson_record.parsed_lesson_type,
                lesson_record.original_dates,
                lesson_record.audience_number,
                lesson_record.building_number,
                lesson_record.discipline_id,
            )

            if lesson_key not in result_dict:
                result_dict[lesson_key] = TeacherLessonExtendedDTO(
                    id=lesson_record.id,
                    created_at=lesson_record.created_at,
                    number_of_day=lesson_record.number_of_day,
                    original_dates=lesson_record.original_dates,
                    parsed_parity=lesson_record.parsed_parity,
                    parsed_dates=lesson_record.parsed_dates,
                    parsed_dates_status=lesson_record.parsed_dates_status,
                    start_time=lesson_record.start_time,
                    end_time=lesson_record.end_time,
                    audience_number=lesson_record.audience_number,
                    building_number=lesson_record.building_number,
                    original_lesson_type=lesson_record.original_lesson_type,
                    parsed_lesson_type=lesson_record.parsed_lesson_type,
                    group_id=lesson_record.group_id,
                    discipline_id=lesson_record.discipline_id,
                    department_id=lesson_record.department_id,
                    teacher_id=lesson_record.teacher_id,
                    groups=[
                        GroupGateway._db_to_entity(lesson_record.group),
                    ],
                    department=DepartmentGateway.db_to_entity(lesson_record.department),
                    discipline=DisciplineGateway._db_to_entity(
                        lesson_record.discipline,
                    ),
                )
            else:
                result_dict[lesson_key].groups.append(
                    GroupGateway._db_to_entity(lesson_record.group),
                )

        for lesson_key in result_dict:
            result_dict[lesson_key].groups.sort(key=lambda x: x.group_name)

        return list(result_dict.values())

    async def get_by_group_id(
        self,
        group_id: str,
        week_parity: WeekParity,
    ) -> list[LessonEntity]:
        if week_parity == WeekParity.ANY:
            parities = {WeekParity.ANY, WeekParity.ODD, WeekParity.EVEN}
        else:
            parities = {WeekParity.ANY, week_parity}

        stmt = (
            select(LessonModel)
            .where(
                LessonModel.group_id == group_id,
                LessonModel.parsed_parity.in_(parities),
            )
            .order_by(LessonModel.number_of_day, LessonModel.start_time)
        )
        lessons = await self._session.scalars(stmt)

        return [self._db_to_entity(lesson) for lesson in lessons.all()]

    async def get_by_id_extended(self, lesson_id: str) -> LessonExtendedDTO:
        stmt = (
            select(LessonModel)
            .where(LessonModel.id == lesson_id)
            .options(
                selectinload(LessonModel.discipline),
                selectinload(LessonModel.department),
                selectinload(LessonModel.teacher),
            )
        )
        return self._db_to_extended_dto(await self._session.scalar(stmt))

    async def get_by_teacher_id_extended(
        self,
        teacher_id: str,
        week_parity: WeekParity,
    ) -> list[TeacherLessonExtendedDTO]:
        if week_parity == WeekParity.ANY:
            parities = {WeekParity.ANY, WeekParity.ODD, WeekParity.EVEN}
        else:
            parities = {WeekParity.ANY, week_parity}

        stmt = (
            select(LessonModel)
            .where(
                LessonModel.teacher_id == teacher_id,
                LessonModel.parsed_parity.in_(parities),
            )
            .order_by(LessonModel.number_of_day, LessonModel.start_time)
            .options(
                selectinload(LessonModel.discipline),
                selectinload(LessonModel.department),
                selectinload(LessonModel.group),
            )
        )
        lessons = await self._session.scalars(stmt)

        return self.db_to_teacher_extended_dto(lessons)

    async def get_by_group_id_extended(
        self,
        group_id: str,
        week_parity: WeekParity,
    ) -> list[LessonExtendedDTO]:
        if week_parity == WeekParity.ANY:
            parities = {WeekParity.ANY, WeekParity.ODD, WeekParity.EVEN}
        else:
            parities = {WeekParity.ANY, week_parity}

        stmt = (
            select(LessonModel)
            .where(
                LessonModel.group_id == group_id,
                LessonModel.parsed_parity.in_(parities),
            )
            .order_by(LessonModel.number_of_day, LessonModel.start_time)
            .options(
                selectinload(LessonModel.discipline),
                selectinload(LessonModel.department),
                selectinload(LessonModel.teacher),
            )
        )
        lessons = await self._session.scalars(stmt)

        return [self._db_to_extended_dto(lesson) for lesson in lessons.all()]

    async def save(self, lesson: LessonEntity) -> None:
        await self._session.execute(
            insert(LessonModel).values(**dataclasses.asdict(lesson)),
        )

    async def update(self, lesson: LessonEntity) -> None:
        update_dict = dataclasses.asdict(lesson)
        update_dict.pop('id')

        try:
            await self._session.execute(
                update(LessonModel)
                .where(LessonModel.id == lesson.id)
                .values(**update_dict),
            )
        except IntegrityError:
            raise BadRelatedEntityError

    async def patch(self, lesson_id: str, lesson_patch: LessonPatchDTO) -> None:
        try:
            await self._session.execute(
                update(LessonModel)
                .where(LessonModel.id == lesson_id)
                .values(**lesson_patch.model_dump(exclude_unset=True)),
            )
        except IntegrityError:
            raise BadRelatedEntityError

    async def delete(self, lesson_id: str) -> None:
        await self._session.execute(
            delete(LessonModel).where(LessonModel.id == lesson_id),
        )
