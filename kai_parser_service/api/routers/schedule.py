from fastapi import APIRouter, HTTPException

from api.dependencies import KaiParserDep
from api.schemas.schedule import LessonRead
from utils.kai_parser.schemas.errors import KaiApiError


router = APIRouter()


@router.get(
    '',
    response_model=list[LessonRead]
)
async def get_schedule(
    group_kai_id: str,
    kai_parser: KaiParserDep
):
    try:
        return await kai_parser.parse_group_schedule(group_kai_id=group_kai_id)
    except KaiApiError:
        raise HTTPException(status_code=530, detail='KAI unreachable')
