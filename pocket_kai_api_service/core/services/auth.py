from datetime import datetime

from uuid import uuid4

from abc import ABC, abstractmethod

from core.exceptions.base import EntityNotFoundError
from core.repositories.group import GroupRepositoryBase
from core.repositories.kai_user import KaiUserRepositoryBase
from core.repositories.pocket_kai_user import PocketKaiUserRepositoryBase
from core.repositories.refresh_token import RefreshTokenRepositoryBase
from core.security.jwt import JWTManagerProtocol
from core.unit_of_work import UnitOfWorkBase
from utils.kai_parser_api.api import KaiParserApi


class AuthServiceBase(ABC):
    def __init__(
        self,
        pocket_kai_user_repository: PocketKaiUserRepositoryBase,
        kai_user_repository: KaiUserRepositoryBase,
        refresh_token_repository: RefreshTokenRepositoryBase,
        group_repository: GroupRepositoryBase,
        uow: UnitOfWorkBase,
        kai_parser_api: KaiParserApi,
        jwt_manager: JWTManagerProtocol,
    ):
        self.pocket_kai_user_repository = pocket_kai_user_repository
        self.kai_user_repository = kai_user_repository
        self.refresh_token_repository = refresh_token_repository
        self.group_repository = group_repository
        self.uow = uow
        self.kai_parser_api = kai_parser_api
        self.jwt_manager = jwt_manager

    @abstractmethod
    async def login_by_kai(self, username: str, password: str) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def refresh_token_pair(self, refresh_token: str) -> tuple[str, str]:
        raise NotImplementedError


class AuthService(AuthServiceBase):
    async def login_by_kai(self, username: str, password: str) -> tuple[str, str]:
        user_about, user_info = await self.kai_parser_api.kai_login(username, password)

        try:
            kai_user = await self.kai_user_repository.get_by_email(
                email=user_info.email,
            )
        except EntityNotFoundError:
            group = await self.group_repository.get_by_name(
                group_name=str(user_about.groupNum),
            )

            kai_user = await self.kai_user_repository.create(
                kai_id=user_about.studId,
                position=None,
                login=username,
                password=password,
                full_name=user_info.full_name,
                phone=user_info.phone,
                email=user_info.email,
                sex=user_info.sex,
                birthday=user_info.birthday,
                is_leader=False,
                zach_number=user_about.zach,
                competition_type=user_about.competitionType,
                contract_number=user_about.numDog,
                edu_level=user_about.eduLevel,
                edu_cycle=user_about.eduCycle,
                edu_qualification=user_about.eduQualif,
                program_form=user_about.programForm,
                status=user_about.status,
                group_id=group.id,
                pocket_kai_user_id=None,
            )

        if kai_user.pocket_kai_user_id is None:
            pocket_kai_user = await self.pocket_kai_user_repository.create(
                telegram_id=None,
                phone=None,
                is_blocked=False,
            )

            kai_user.pocket_kai_user_id = pocket_kai_user.id
            kai_user = await self.kai_user_repository.update(kai_user)
        else:
            pocket_kai_user = await self.pocket_kai_user_repository.get_by_id(
                kai_user.pocket_kai_user_id,
            )

        access_token = self.jwt_manager.create_access_token(
            user_id=str(pocket_kai_user.id),
        )
        refresh_token_id = uuid4()
        refresh_token = self.jwt_manager.create_refresh_token(
            jti=str(refresh_token_id),
            user_id=str(pocket_kai_user.id),
        )
        refresh_token_payload = self.jwt_manager.decode_refresh_token(refresh_token)

        await self.refresh_token_repository.create(
            id=refresh_token_id,
            token=refresh_token,
            name=None,
            issued_at=refresh_token_payload.iat,
            expires_at=refresh_token_payload.exp,
            pocket_kai_user_id=pocket_kai_user.id,
        )
        await self.uow.commit()

        return access_token, refresh_token

    async def refresh_token_pair(self, refresh_token: str) -> tuple[str, str]:
        refresh_token_payload = self.jwt_manager.decode_refresh_token(refresh_token)
        pocket_kai_user = await self.pocket_kai_user_repository.get_by_id(
            refresh_token_payload.sub,
        )

        refresh_token = await self.refresh_token_repository.get_by_id(
            refresh_token_payload.jti,
        )
        # Время жизни обновляется
        new_refresh_token = self.jwt_manager.create_refresh_token(
            jti=str(refresh_token_payload.jti),
            user_id=str(pocket_kai_user.id),
        )
        new_refresh_token_payload = self.jwt_manager.decode_refresh_token(
            new_refresh_token,
        )

        refresh_token.expires_at = new_refresh_token_payload.exp.replace(tzinfo=None)
        refresh_token.issued_at = new_refresh_token_payload.iat.replace(tzinfo=None)
        refresh_token.last_used_at = datetime.utcnow()
        refresh_token.token = new_refresh_token
        await self.refresh_token_repository.update(refresh_token)

        await self.uow.commit()

        new_access_token = self.jwt_manager.create_access_token(
            user_id=str(pocket_kai_user.id),
        )
        return new_access_token, new_refresh_token
