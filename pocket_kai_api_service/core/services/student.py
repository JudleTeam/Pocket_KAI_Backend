from datetime import date

from uuid import UUID

from abc import ABC, abstractmethod

from core.entities.student import StudentEntity
from core.repositories.student import StudentRepositoryBase


class StudentServiceBase(ABC):
    def __init__(
        self,
        student_repository: StudentRepositoryBase,
    ):
        self.student_repository = student_repository

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> StudentEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> StudentEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, updated_student: StudentEntity) -> StudentEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID) -> list[StudentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        full_name: str,
        email: str,
        kai_id: int | None = None,
        position: int | None = None,
        login: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        sex: str | None = None,
        birthday: date | None = None,
        is_leader: bool = False,
        zach_number: str | None = None,
        competition_type: str | None = None,
        contract_number: str | None = None,
        edu_level: str | None = None,
        edu_cycle: str | None = None,
        edu_qualification: str | None = None,
        program_form: str | None = None,
        status: str | None = None,
        group_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> StudentEntity:
        raise NotImplementedError


class StudentService(StudentServiceBase):
    async def get_by_user_id(self, user_id: UUID) -> StudentEntity:
        return await self.student_repository.get_by_user_id(user_id)

    async def get_by_group_id(self, group_id: UUID) -> list[StudentEntity]:
        return await self.student_repository.list(filters={'group_id': group_id})

    async def update(self, updated_student: StudentEntity) -> StudentEntity:
        return await self.student_repository.update(updated_student)

    async def create(
        self,
        full_name: str,
        email: str,
        kai_id: int | None = None,
        position: int | None = None,
        login: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        sex: str | None = None,
        birthday: date | None = None,
        is_leader: bool = False,
        zach_number: str | None = None,
        competition_type: str | None = None,
        contract_number: str | None = None,
        edu_level: str | None = None,
        edu_cycle: str | None = None,
        edu_qualification: str | None = None,
        program_form: str | None = None,
        status: str | None = None,
        group_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> StudentEntity:
        return await self.student_repository.create(
            kai_id=kai_id,
            position=position,
            login=login,
            password=password,
            full_name=full_name,
            phone=phone,
            email=email,
            sex=sex,
            birthday=birthday,
            is_leader=is_leader,
            zach_number=zach_number,
            competition_type=competition_type,
            contract_number=contract_number,
            edu_level=edu_level,
            edu_cycle=edu_cycle,
            edu_qualification=edu_qualification,
            program_form=program_form,
            status=status,
            group_id=group_id,
            user_id=user_id,
        )

    async def get_by_email(self, email: str) -> StudentEntity:
        return await self.student_repository.get_by_email(email)
