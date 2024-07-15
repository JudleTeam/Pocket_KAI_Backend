from sqlalchemy import select
from uuid import UUID

from datetime import date

from abc import ABC

from core.entities.student import StudentEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import StudentModel


class StudentRepositoryBase(GenericRepository[StudentEntity], ABC):
    entity = StudentEntity

    async def create(
        self,
        kai_id: int | None,
        position: int | None,
        login: str | None,
        password: str | None,
        full_name: str,
        phone: str | None,
        email: str,
        sex: str | None,
        birthday: date | None,
        is_leader: bool,
        zach_number: str | None,
        competition_type: str | None,
        contract_number: str | None,
        edu_level: str | None,
        edu_cycle: str | None,
        edu_qualification: str | None,
        program_form: str | None,
        status: str | None,
        group_id: UUID | None,
        user_id: UUID | None,
    ) -> StudentEntity:
        raise NotImplementedError

    async def get_by_login(self, login: str) -> StudentEntity:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> StudentEntity:
        raise NotImplementedError

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> StudentEntity:
        raise NotImplementedError


class SAStudentRepository(GenericSARepository[StudentEntity], StudentRepositoryBase):
    model_cls = StudentModel

    async def create(
        self,
        kai_id: int | None,
        position: int | None,
        login: str | None,
        password: str | None,
        full_name: str,
        phone: str | None,
        email: str,
        sex: str | None,
        birthday: date | None,
        is_leader: bool,
        zach_number: str | None,
        competition_type: str | None,
        contract_number: str | None,
        edu_level: str | None,
        edu_cycle: str | None,
        edu_qualification: str | None,
        program_form: str | None,
        status: str | None,
        group_id: UUID | None,
        user_id: UUID | None,
    ) -> StudentEntity:
        student = StudentModel(
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
        await self._add(student)
        return await self._convert_db_to_entity(student)

    async def get_by_login(self, login: str) -> StudentEntity:
        stmt = select(StudentModel).where(StudentModel.login == login)
        student = await self._session.scalar(stmt)
        if student is None:
            raise EntityNotFoundError(entity=StudentEntity, find_query=login)
        return await self._convert_db_to_entity(student)

    async def get_by_email(self, email: str) -> StudentEntity:
        stmt = select(StudentModel).where(StudentModel.email == email)
        student = await self._session.scalar(stmt)
        if student is None:
            raise EntityNotFoundError(entity=StudentEntity, find_query=email)
        return await self._convert_db_to_entity(student)

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> StudentEntity:
        stmt = select(StudentModel).where(StudentModel.user_id == user_id)
        student = await self._session.scalar(stmt)
        if student is None:
            raise EntityNotFoundError(
                entity=StudentEntity,
                find_query=user_id,
            )
        return await self._convert_db_to_entity(student)
