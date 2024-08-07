from dataclasses import asdict

from pocket_kai.application.dto.lesson import (
    LessonExtendedDTO,
    NewLessonDTO,
    TeacherLessonExtendedDTO,
)
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.department import DepartmentReader
from pocket_kai.application.interfaces.entities.discipline import DisciplineReader
from pocket_kai.application.interfaces.entities.lesson import (
    LessonDeleter,
    LessonGatewayProtocol,
    LessonReader,
    LessonSaver,
)
from pocket_kai.application.interfaces.entities.teacher import TeacherReader
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.entitites.lesson import LessonEntity
from pocket_kai.domain.exceptions.lesson import LessonNotFoundError
from pocket_kai.domain.exceptions.teacher import TeacherNotFoundError


class ExtendedLessonConverter:
    def __init__(
        self,
        teacher_gateway: TeacherReader,
        department_gateway: DepartmentReader,
        discipline_gateway: DisciplineReader,
    ):
        self._teacher_gateway = teacher_gateway
        self._department_gateway = department_gateway
        self._discipline_gateway = discipline_gateway

    async def __call__(self, entity: LessonEntity) -> LessonExtendedDTO:
        return LessonExtendedDTO(
            **asdict(entity),
            teacher=await self._teacher_gateway.get_by_id(entity.teacher_id)
            if entity.teacher_id
            else None,
            department=await self._department_gateway.get_by_id(
                entity.department_id,
            )
            if entity.department_id
            else None,
            discipline=await self._discipline_gateway.get_by_id(
                entity.discipline_id,
            ),
        )


class GetLessonsByGroupIdInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
    ):
        self._lesson_gateway = lesson_gateway

    async def __call__(self, group_id: str) -> list[LessonExtendedDTO]:
        return await self._lesson_gateway.get_by_group_id_extended(
            group_id,
            week_parity=WeekParity.ANY,
        )


class CreateLessonInteractor:
    def __init__(
        self,
        lesson_gateway: LessonSaver,
        extended_lesson_converter: ExtendedLessonConverter,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self._lesson_gateway = lesson_gateway
        self._extended_lesson_converter = extended_lesson_converter

        self._uow = uow
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager

    async def __call__(self, new_lesson: NewLessonDTO) -> LessonExtendedDTO:
        lesson = LessonEntity(
            id=self._uuid_generator(),
            created_at=self._datetime_manager.now(),
            number_of_day=new_lesson.number_of_day,
            original_dates=new_lesson.original_dates,
            parsed_parity=new_lesson.parsed_parity,
            parsed_dates=new_lesson.parsed_dates,
            parsed_dates_status=new_lesson.parsed_dates_status,
            audience_number=new_lesson.audience_number,
            building_number=new_lesson.building_number,
            original_lesson_type=new_lesson.original_lesson_type,
            parsed_lesson_type=new_lesson.parsed_lesson_type,
            start_time=new_lesson.start_time,
            end_time=new_lesson.end_time,
            discipline_id=new_lesson.discipline_id,
            teacher_id=new_lesson.teacher_id,
            department_id=new_lesson.department_id,
            group_id=new_lesson.group_id,
        )
        await self._lesson_gateway.save(lesson)
        await self._uow.commit()

        return await self._extended_lesson_converter(lesson)


class DeleteLessonInteractor:
    def __init__(
        self,
        lesson_gateway: LessonDeleter,
        uow: UnitOfWork,
    ):
        self._lesson_gateway = lesson_gateway
        self._uow = uow

    async def __call__(self, lesson_id: str) -> None:
        await self._lesson_gateway.delete(lesson_id)
        await self._uow.commit()


class UpdateLessonInteractor:
    def __init__(
        self,
        lesson_gateway: LessonGatewayProtocol,
        extended_lesson_converter: ExtendedLessonConverter,
        uow: UnitOfWork,
    ):
        self._lesson_gateway = lesson_gateway
        self._lesson_extended_converter = extended_lesson_converter

        self._uow = uow

    async def __call__(self, lesson_entity: LessonEntity) -> LessonExtendedDTO:
        lesson = await self._lesson_gateway.get_by_id_extended(lesson_entity.id)
        if lesson is None:
            raise LessonNotFoundError

        await self._lesson_gateway.update(lesson_entity)
        await self._uow.commit()
        return await self._lesson_extended_converter(lesson_entity)


class GetLessonsByTeacherIdInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
        teacher_gateway: TeacherReader,
    ):
        self._lesson_gateway = lesson_gateway
        self._teacher_gateway = teacher_gateway

    async def __call__(
        self,
        teacher_id: str,
        week_parity: WeekParity,
    ) -> list[TeacherLessonExtendedDTO]:
        teacher = await self._teacher_gateway.get_by_id(id=teacher_id)
        if teacher is None:
            raise TeacherNotFoundError

        return await self._lesson_gateway.get_by_teacher_id_extended(
            teacher_id=teacher_id,
            week_parity=week_parity,
        )
