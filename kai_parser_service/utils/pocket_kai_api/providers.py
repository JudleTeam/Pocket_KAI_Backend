from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from config import Settings, get_settings
from utils.pocket_kai_api.api import PocketKaiApi


async def get_pocket_kai_api(
    settings: Annotated[Settings, Depends(get_settings)],
):
    async with ClientSession() as session:
        yield PocketKaiApi(
            base_url=settings.pocket_kai_base_url,
            session=session,
        )
