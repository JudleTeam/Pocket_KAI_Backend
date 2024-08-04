from pocket_kai.application.dto.teacher import NewTeacherDTO
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.teacher import (
    TeacherReader,
    TeacherSaver,
)
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.teacher import TeacherEntity
from pocket_kai.domain.exceptions.teacher import TeacherNotFoundError


class GetTeacherByLoginInteractor:
    def __init__(
        self,
        teacher_gateway: TeacherReader,
    ):
        self._teacher_gateway = teacher_gateway

    async def __call__(self, login: str) -> TeacherEntity:
        teacher = await self._teacher_gateway.get_by_login(login)
        if teacher is None:
            raise TeacherNotFoundError
        return teacher


class SuggestTeachersByNameInteractor:
    def __init__(
        self,
        teacher_gateway: TeacherReader,
    ):
        self._teacher_gateway = teacher_gateway

    async def __call__(self, name: str, limit: int) -> list[TeacherEntity]:
        return await self._teacher_gateway.suggest_by_name(name=name, limit=limit)


class CreateTeacherInteractor:
    def __init__(
        self,
        teacher_gateway: TeacherSaver,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self._teacher_gateway = teacher_gateway
        self._uow = uow
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager

    async def __call__(self, teacher: NewTeacherDTO) -> TeacherEntity:
        teacher_entity = TeacherEntity(
            id=self._uuid_generator(),
            created_at=self._datetime_manager.now(),
            login=teacher.login,
            name=teacher.name,
        )
        await self._teacher_gateway.save(teacher_entity)
        await self._uow.commit()

        return teacher_entity
