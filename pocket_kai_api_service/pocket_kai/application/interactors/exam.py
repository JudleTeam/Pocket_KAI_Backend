from dataclasses import asdict

from pocket_kai.application.dto.exam import ExamExtendedDTO, NewExamDTO, UpdateExamDTO
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.exam import (
    ExamDeleter,
    ExamGatewayProtocol,
    ExamReader,
)
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.exam import ExamEntity
from pocket_kai.domain.exceptions.exam import ExamNotFoundError


class CreateExamInteractor:
    def __init__(
        self,
        exam_gateway: ExamGatewayProtocol,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self._exam_gateway = exam_gateway
        self._uow = uow
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager

    async def __call__(
        self,
        dto: NewExamDTO,
    ) -> ExamExtendedDTO:
        new_exam = ExamEntity(
            id=self._uuid_generator(),
            created_at=self._datetime_manager.now(),
            **asdict(dto),
        )

        await self._exam_gateway.save(new_exam)
        await self._uow.commit()

        return await self._exam_gateway.get_by_id_extended(new_exam.id)


class UpdateExamInteractor:
    def __init__(
        self,
        exam_gateway: ExamGatewayProtocol,
        uow: UnitOfWork,
    ):
        self._exam_gateway = exam_gateway
        self._uow = uow

    async def __call__(self, exam_update: UpdateExamDTO) -> ExamExtendedDTO:
        exam_entity = ExamEntity(**asdict(exam_update))
        await self._exam_gateway.update(exam_entity)
        await self._uow.commit()

        exam_entity = await self._exam_gateway.get_by_id_extended(exam_update.id)
        if exam_entity is None:
            raise ExamNotFoundError

        return exam_entity


class GetExamsByGroupIdInteractor:
    def __init__(
        self,
        exam_gateway: ExamReader,
    ):
        self._exam_gateway = exam_gateway

    async def __call__(
        self,
        group_id: str,
        academic_year: str | None,
        academic_year_half: int | None,
    ) -> list[ExamExtendedDTO]:
        return await self._exam_gateway.get_by_group_id_extended(
            group_id,
            academic_year=academic_year,
            academic_year_half=academic_year_half,
        )


class DeleteExamInteractor:
    def __init__(
        self,
        exam_gateway: ExamDeleter,
        uow: UnitOfWork,
    ):
        self._exam_gateway = exam_gateway
        self._uow = uow

    async def __call__(self, exam_id: str) -> None:
        await self._exam_gateway.delete(exam_id)
        await self._uow.commit()
