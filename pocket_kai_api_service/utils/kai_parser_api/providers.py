from aiohttp import ClientSession
from fastapi import Depends
from typing import Annotated

from config import Settings, get_settings
from utils.common import get_session
from utils.kai_parser_api.api import KaiParserApi


def get_kai_parser_api(
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[ClientSession, Depends(get_session)],
):
    yield KaiParserApi(
        base_url=settings.KAI_PARSER_API_BASE_URL,
        session=session,
    )
