from sqlalchemy import select
from uuid import UUID

from datetime import date

from abc import ABC

from core.entities.kai_user import KaiUserEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import KAIUser


class KaiUserRepositoryBase(GenericRepository[KaiUserEntity], ABC):
    entity = KaiUserEntity

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
        pocket_kai_user_id: UUID | None,
    ) -> KaiUserEntity:
        raise NotImplementedError

    async def get_by_login(self, login: str) -> KaiUserEntity:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> KaiUserEntity:
        raise NotImplementedError

    async def get_by_pocket_kai_user_id(
        self,
        pocket_kai_user_id: UUID,
    ) -> KaiUserEntity:
        raise NotImplementedError


class SAKaiUserRepository(GenericSARepository[KaiUserEntity], KaiUserRepositoryBase):
    model_cls = KAIUser

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
        pocket_kai_user_id: UUID | None,
    ) -> KaiUserEntity:
        kai_user = KAIUser(
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
            pocket_kai_user_id=pocket_kai_user_id,
        )

        await self._add(kai_user)

        return await self._convert_db_to_entity(kai_user)

    async def get_by_login(self, login: str) -> KaiUserEntity:
        stmt = select(KAIUser).where(KAIUser.login == login)
        kai_user = await self._session.scalar(stmt)
        if kai_user is None:
            raise EntityNotFoundError(entity=KaiUserEntity, find_query=login)
        return await self._convert_db_to_entity(kai_user)

    async def get_by_email(self, email: str) -> KaiUserEntity:
        stmt = select(KAIUser).where(KAIUser.email == email)
        kai_user = await self._session.scalar(stmt)
        if kai_user is None:
            raise EntityNotFoundError(entity=KaiUserEntity, find_query=email)
        return await self._convert_db_to_entity(kai_user)

    async def get_by_pocket_kai_user_id(
        self,
        pocket_kai_user_id: UUID,
    ) -> KaiUserEntity:
        stmt = select(KAIUser).where(KAIUser.pocket_kai_user_id == pocket_kai_user_id)
        kai_user = await self._session.scalar(stmt)
        if kai_user is None:
            raise EntityNotFoundError(
                entity=KaiUserEntity,
                find_query=pocket_kai_user_id,
            )
        return await self._convert_db_to_entity(kai_user)
