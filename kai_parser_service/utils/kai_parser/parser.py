import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncIterator

from aiohttp import ClientError, ClientResponse, ClientSession

from core.exceptions.common import RetryError
from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.helper import get_year_data_from_group_name
from utils.kai_parser.schemas.errors import KaiApiError
from utils.kai_parser.schemas.exam import ParsedExam, ParsedGroupExams
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
        timeout: int = 30,
    ):
        self.session = session
        self.request_retries = request_retries
        self.timeout = timeout

    @asynccontextmanager
    async def _request(
        self,
        method,
        url,
        *,
        current_retry=0,
        **kwargs,
    ) -> AsyncIterator[ClientResponse]:
        try:
            async with self.session.request(
                method=method,
                url=url,
                **kwargs,
                timeout=self.timeout,
            ) as response:
                if not response.ok:
                    raise RetryError
                yield response

        except (asyncio.TimeoutError, ClientError, RetryError):
            if current_retry < self.request_retries:
                async with self._request(
                    method,
                    url,
                    current_retry=current_retry + 1,
                    **kwargs,
                ) as response:
                    yield response
            raise KaiApiError(f'URL: {url} | Status: {response.status}')

    async def _awaitable_request(self, **kwargs):
        async with self._request(**kwargs) as response:
            return response

    async def parse_groups(self) -> list[ParsedGroup]:
        request_params = {
            'p_p_id': 'pubStudentSchedule_WAR_publicStudentSchedule10',
            'p_p_lifecycle': 2,
            'p_p_resource_id': 'getGroupsURL',
        }

        async with self._request(
            'GET',
            self.schedule_url,
            params=request_params,
        ) as response:
            groups_from_kai = await response.json(content_type='text/html')

        return [
            ParsedGroup(
                forma=group.get('forma'),
                name=group.get('group'),
                id=group.get('id'),
            )
            for group in groups_from_kai
        ]

    async def parse_group_schedule(self, group_kai_id: int) -> ParsedGroupSchedule:
        params = {
            'p_p_id': 'pubStudentSchedule_WAR_publicStudentSchedule10',
            'p_p_lifecycle': 2,
            'p_p_resource_id': 'schedule',
        }
        data = {
            'groupId': group_kai_id,
        }

        parsed_at = datetime.now(timezone.utc)
        async with self._request(
            'POST',
            self.schedule_url,
            params=params,
            data=data,
        ) as response:
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
            )
            for day_lessons in lessons_from_kai.values()
            for lesson in day_lessons
        ]

        return ParsedGroupSchedule(
            parsed_at=parsed_at,
            group_kai_id=group_kai_id,
            lessons=lessons,
        )

    async def parse_group_exams(self, group_kai_id: int, group_name: str):
        params = {
            'p_p_id': 'pubStudentSchedule_WAR_publicStudentSchedule10',
            'p_p_lifecycle': 2,
            'p_p_resource_id': 'examSchedule',
        }
        data = {
            'groupId': group_kai_id,
        }

        parsed_at = datetime.now(timezone.utc)
        async with self._request(
            'POST',
            self.schedule_url,
            params=params,
            data=data,
        ) as response:
            exams_from_kai = await response.json(content_type='text/html')

        parsed_exams = [
            ParsedExam(
                date=exam.get('examDate'),
                time=exam.get('examTime'),
                discipline_name=exam.get('disciplName'),
                discipline_number=exam.get('disciplNum'),
                audience_number=exam.get('audNum'),
                building_number=exam.get('buildNum'),
                teacher_name=exam.get('prepodName'),
                teacher_login=exam.get('prepodLogin'),
            )
            for exam in exams_from_kai
        ]

        return ParsedGroupExams(
            parsed_at=parsed_at,
            group_kai_id=group_kai_id,
            parsed_exams=parsed_exams,
            year_data=get_year_data_from_group_name(group_name),
        )
