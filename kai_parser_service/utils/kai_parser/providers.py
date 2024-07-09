from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from config import Settings, get_settings
from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.parser import KaiParser


async def get_kai_parser(
    settings: Annotated[Settings, Depends(get_settings)],
) -> KaiParserBase:
    async with ClientSession() as session:
        yield KaiParser(
            session=session,
            timeout=settings.timeout_seconds,
            request_retries=settings.request_retries,
        )
