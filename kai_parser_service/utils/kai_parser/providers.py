from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from config import Settings, get_settings
from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.parser import KaiParser
from utils.kai_parser.user_parser import KaiUserParser


async def get_kai_parser(
    settings: Annotated[Settings, Depends(get_settings)],
) -> KaiParserBase:
    async with ClientSession() as session:
        yield KaiParser(
            session=session,
            timeout=settings.TIMEOUT_SECONDS,
            request_retries=settings.REQUEST_RETRIES,
        )


async def get_kai_user_parser(
    settings: Annotated[Settings, Depends(get_settings)],
) -> KaiUserParser:
    async with ClientSession() as session:
        yield KaiUserParser(
            session=session,
            max_retries=settings.REQUEST_RETRIES,
        )
