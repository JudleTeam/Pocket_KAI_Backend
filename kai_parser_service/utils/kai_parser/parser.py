import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal

from aiohttp import ClientError, ClientSession

from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.schemas.errors import KaiApiError
from utils.kai_parser.schemas.group import ParsedGroup
from utils.kai_parser.schemas.lesson import ParsedLesson
from utils.kai_parser.schemas.schedule import ParsedGroupSchedule


class KaiParser(KaiParserBase):
    schedule_url = 'https://kai.ru/raspisanie'
    about_me_url = 'https://kai.ru/group/guest/common/about-me'
    my_group_url = 'https://kai.ru/group/guest/student/moa-gruppa'
    kai_main_url = 'https://kai.ru/main'
    syllabus_url = 'https://kai.ru/group/guest/student/ucebnyj-plan'

    def __init__(
        self,
        session: ClientSession,
        request_retries: int = 3,
        timeout: int = 30
    ):
        self.session = session
        self.request_retries = request_retries
        self.timeout = timeout

    @asynccontextmanager
    async def _send_request(
        self,
        method: Literal['GET', 'POST'],
        url: str, params: dict = None,
        data=None, json=None
    ):
        async with self.session.request(
                method, url, timeout=self.timeout, params=params, data=data, json=json
        ) as response:
            if not response.ok:
                raise KaiApiError
            yield response

    @asynccontextmanager
    async def _request(
        self,
        method: Literal['GET', 'POST'],
        url: str, params: dict = None,
        data=None, json=None, current_retry=0
    ):
        try:
            async with self._send_request(method, url, params, data, json) as response:
                yield response
        except (asyncio.TimeoutError, ClientError, KaiApiError):
            if current_retry < self.request_retries:
                async with self._request(method, url, params, data, json, current_retry + 1) as retry_response:
                    yield retry_response
            else:
                raise KaiApiError

    async def parse_groups(self) -> list[ParsedGroup]:
        request_params = {
            'p_p_id'         : 'pubStudentSchedule_WAR_publicStudentSchedule10',
            'p_p_lifecycle'  : 2,
            'p_p_resource_id': 'getGroupsURL'
        }

        async with self._request('GET', self.schedule_url, params=request_params) as response:
            groups_from_kai = await response.json(content_type='text/html')

        return [
            ParsedGroup(
                forma=group.get('forma'),
                name=group.get('group'),
                id=group.get('id'),
            ) for group in groups_from_kai
        ]

    async def parse_group_schedule(self, group_kai_id: int) -> ParsedGroupSchedule:
        params = {
            'p_p_id'         : 'pubStudentSchedule_WAR_publicStudentSchedule10',
            'p_p_lifecycle'  : 2,
            'p_p_resource_id': 'schedule'
        }
        data = {
            'groupId': group_kai_id
        }

        parsed_at = datetime.now(timezone.utc)
        async with self._request('POST', self.schedule_url, params=params, data=data) as response:
            lessons_from_kai = await response.json(content_type='text/html')

        lessons = [
            ParsedLesson(
                day_number=lesson.get('dayNum'),
                start_time=lesson.get('dayTime'),
                dates=lesson.get('dayDate'),
                discipline_name=lesson.get('disciplName'),
                audience_number=lesson.get('audNum'),
                building_number=lesson.get('buildNum'),
                discipline_type=lesson.get('disciplType'),
                discipline_number=lesson.get('disciplNum'),
                department_id=lesson.get('orgUnitId'),
                teacher_name=lesson.get('prepodName'),
                teacher_login=lesson.get('prepodLogin'),
                department_name=lesson.get('orgUnitName'),
            ) for day_lessons in lessons_from_kai.values() for lesson in day_lessons
        ]

        return ParsedGroupSchedule(
            parsed_at=parsed_at,
            group_kai_id=group_kai_id,
            lessons=lessons
        )

