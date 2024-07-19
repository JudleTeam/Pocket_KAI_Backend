import aiohttp
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, from_context, provide

from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.jwt import JWTManagerProtocol
from pocket_kai.application.interfaces.kai_parser_api import KaiParserApiProtocol
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.config import Settings
from pocket_kai.infrastructure.database.database import new_session_maker
from pocket_kai.infrastructure.jwt import PyJWTManager
from pocket_kai.infrastructure.kai_parser_api.api import KaiParserApi
from pocket_kai.ioc.gateways import GatewaysProvider
from pocket_kai.ioc.interactors import InteractorsProvider
from pocket_kai.infrastructure.datetime_manager import UTCDateTimeManager


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_datetime_manager(self) -> DateTimeManager:
        return UTCDateTimeManager()

    @provide(scope=Scope.APP)
    def get_jwt_manager(
        self,
        settings: Settings,
        datetime_manager: DateTimeManager,
    ) -> JWTManagerProtocol:
        return PyJWTManager(
            access_token_expire_minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES,
            private_key=settings.jwt.private_key_path.read_text(),
            public_key=settings.jwt.public_key_path.read_text(),
            algorithm=settings.jwt.JWT_ALGORITHM,
            datetime_manager=datetime_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def get_kai_parser_api(
        self,
        settings: Settings,
    ) -> AsyncIterable[KaiParserApiProtocol]:
        async with aiohttp.ClientSession() as session:
            yield KaiParserApi(
                base_url=settings.kai_parser.KAI_PARSER_API_BASE_URL,
                session=session,
            )

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(
        self,
        settings: Settings,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(postgres_settings=settings.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, UnitOfWork]]:
        async with async_session_maker() as session:
            yield session


providers = (
    AppProvider(),
    GatewaysProvider(),
    InteractorsProvider(),
)
