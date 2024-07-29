from fastapi import APIRouter, HTTPException

from api.dependencies import KaiParserDep
from api.schemas.exam import GroupExamsResponse
from core.exceptions.api import KaiApiError


router = APIRouter()


@router.get(
    '',
    response_model=GroupExamsResponse,
)
async def get_exams_for_group(
    group_kai_id: int,
    group_name: str,
    *,
    kai_parser: KaiParserDep,
):
    try:
        return await kai_parser.parse_group_exams(
            group_kai_id=group_kai_id,
            group_name=group_name,
        )
    except KaiApiError:
        raise HTTPException(status_code=530, detail='KAI unreachable')
