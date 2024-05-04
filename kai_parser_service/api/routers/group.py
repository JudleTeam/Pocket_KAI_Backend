from fastapi import APIRouter, HTTPException

from api.dependencies import KaiParserDep
from api.schemas.group import GroupRead
from utils.kai_parser.schemas.errors import KaiApiError


router = APIRouter()


@router.get(
    '',
    response_model=list[GroupRead]
)
async def get_groups(kai_parser: KaiParserDep):
    try:
        return await kai_parser.parse_groups()
    except KaiApiError:
        raise HTTPException(status_code=530, detail='KAI unreachable')
