from typing import Annotated

from fastapi import Depends

from core.services.group import GroupServiceBase
from core.services.providers import get_schedule_service, get_group_service
from core.services.schedule import ScheduleServiceBase


GroupServiceDep = Annotated[GroupServiceBase, Depends(get_group_service)]
ScheduleServiceDep = Annotated[ScheduleServiceBase, Depends(get_schedule_service)]
