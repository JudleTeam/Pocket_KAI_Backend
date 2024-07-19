from pocket_kai.application.dto.discipline import NewDisciplineDTO
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.discipline import (
    DisciplineReader,
    DisciplineSaver,
)
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.discipline import DisciplineEntity
from pocket_kai.domain.exceptions.discipline import DisciplineNotFoundError


class GetDisciplineByKaiIdInteractor:
    def __init__(self, discipline_gateway: DisciplineReader):
        self._discipline_gateway = discipline_gateway

    async def __call__(self, kai_id: int) -> DisciplineEntity:
        discipline = await self._discipline_gateway.get_by_kai_id(kai_id=kai_id)
        if discipline is None:
            raise DisciplineNotFoundError
        return discipline


class CreateDisciplineInteractor:
    def __init__(
        self,
        discipline_gateway: DisciplineSaver,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self._discipline_gateway = discipline_gateway
        self._uow = uow
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager

    async def __call__(self, new_discipline: NewDisciplineDTO) -> DisciplineEntity:
        discipline = DisciplineEntity(
            id=self._uuid_generator(),
            name=new_discipline.name,
            created_at=self._datetime_manager.now(),
            kai_id=new_discipline.kai_id,
        )
        await self._discipline_gateway.save(discipline)
        await self._uow.commit()

        return discipline
