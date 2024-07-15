from typing import Annotated

from fastapi import Depends

from core.services.providers import get_task_service
from core.services.task import TaskServiceBase
from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.providers import get_kai_parser, get_kai_user_parser
from utils.kai_parser.user_parser import KaiUserParser
from utils.pocket_kai_api.api import PocketKaiApi
from utils.pocket_kai_api.providers import get_pocket_kai_api


KaiParserDep = Annotated[KaiParserBase, Depends(get_kai_parser)]
KaiUserParserDep = Annotated[KaiUserParser, Depends(get_kai_user_parser)]
PocketKaiApiDep = Annotated[PocketKaiApi, Depends(get_pocket_kai_api)]

TaskServiceDep = Annotated[TaskServiceBase, Depends(get_task_service)]
