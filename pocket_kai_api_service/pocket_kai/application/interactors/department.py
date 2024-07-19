from pocket_kai.application.dto.department import NewDepartmentDTO
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.department import (
    DepartmentReader,
    DepartmentSaver,
)
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.department import DepartmentEntity
from pocket_kai.domain.exceptions.department import DepartmentNotFoundError


class GetDepartmentByKaiIdInteractor:
    def __init__(self, department_gateway: DepartmentReader):
        self._department_gateway = department_gateway

    async def __call__(self, kai_id: int) -> DepartmentEntity:
        department = await self._department_gateway.get_by_kai_id(kai_id)
        if department is None:
            raise DepartmentNotFoundError

        return department


class CreateDepartmentInteractor:
    def __init__(
        self,
        department_gateway: DepartmentSaver,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self._department_gateway = department_gateway
        self._uow = uow
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager

    async def __call__(self, new_department: NewDepartmentDTO) -> DepartmentEntity:
        department = DepartmentEntity(
            id=self._uuid_generator(),
            created_at=self._datetime_manager.now(),
            kai_id=new_department.kai_id,
            name=new_department.name,
        )
        await self._department_gateway.save(department)
        await self._uow.commit()

        return department
