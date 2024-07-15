import datetime
import logging
from uuid import UUID

from aiohttp import ClientSession

from utils.common import ParsedDatesStatus
from utils.kai_parser_api.schemas import WeekParity
from utils.pocket_kai_api.base import PocketKaiApiBase, PocketKaiApiError
from utils.pocket_kai_api.schemas import (
    PocketKaiDepartment,
    PocketKaiDiscipline,
    PocketKaiGroup,
    PocketKaiLesson,
    PocketKaiTeacher,
)


class PocketKaiApi(PocketKaiApiBase):
    def __init__(
        self,
        session: ClientSession,
        base_pocket_kai_url: str,
        service_token: str,
    ):
        self.session = session
        self.base_pocket_kai_url = base_pocket_kai_url

        self.session.headers.update({'x-service-token': service_token})

    async def _json_request(
        self,
        method: str,
        url: str,
        params: dict = None,
        json: dict = None,
    ) -> dict | None:
        async with self.session.request(
            method,
            url,
            params=params,
            json=json,
        ) as response:
            if response.status in (404, 204):
                return None

            if not response.ok:
                logging.error(
                    f'Pocket kai api request failed. Method: {method}, URL: {url}, Status code: {response.status}\n'
                    f'Params: {params}, Data: {json}\n'
                    f'Answer: {await response.text()}',
                )
                raise PocketKaiApiError(status_code=response.status)

            return await response.json()

    async def add_group(self, group_name: str, group_kai_id: int) -> PocketKaiGroup:
        url = self.base_pocket_kai_url + '/group'
        data = {
            'group_name': group_name,
            'kai_id': group_kai_id,
        }
        result = await self._json_request('post', url, json=data)
        return PocketKaiGroup(**result)

    async def patch_group(
        self,
        group_id: UUID,
        schedule_parsed_at: datetime.datetime | None,
    ) -> PocketKaiGroup:
        url = self.base_pocket_kai_url + f'/group/by_id/{group_id}'
        data = {
            'schedule_parsed_at': schedule_parsed_at.replace(tzinfo=None).isoformat()
            if schedule_parsed_at
            else None,
        }
        result = await self._json_request('PATCH', url, json=data)
        return PocketKaiGroup(**result)

    async def get_group_lessons_by_group_id(
        self,
        group_id: UUID,
    ) -> list[PocketKaiLesson]:
        url = self.base_pocket_kai_url + f'/group/by_id/{group_id}/lesson'
        result = await self._json_request('get', url)
        return [PocketKaiLesson(**lesson_dict) for lesson_dict in result]

    async def get_discipline_by_kai_id(self, kai_id: int) -> PocketKaiDiscipline | None:
        url = self.base_pocket_kai_url + f'/discipline/by_kai_id/{kai_id}'
        result = await self._json_request('get', url)
        return PocketKaiDiscipline(**result) if result else None

    async def add_discipline(self, name: str, kai_id: int) -> PocketKaiDiscipline:
        url = self.base_pocket_kai_url + '/discipline'
        data = {
            'name': name,
            'kai_id': kai_id,
        }
        result = await self._json_request('post', url, json=data)
        return PocketKaiDiscipline(**result)

    async def create_or_get_discipline_by_kai_id(
        self,
        name: str,
        kai_id: int,
    ) -> PocketKaiDiscipline:
        try:
            return await self.add_discipline(name, kai_id)
        except PocketKaiApiError as e:
            if e.status_code == 409:
                return await self.get_discipline_by_kai_id(kai_id)
            raise e

    async def get_department_by_kai_id(self, kai_id: int) -> PocketKaiDepartment | None:
        url = self.base_pocket_kai_url + f'/department/by_kai_id/{kai_id}'
        result = await self._json_request('get', url)
        return PocketKaiDepartment(**result) if result else None

    async def add_department(self, name: str, kai_id: int) -> PocketKaiDepartment:
        url = self.base_pocket_kai_url + '/department'
        data = {
            'name': name,
            'kai_id': kai_id,
        }
        result = await self._json_request('post', url, json=data)
        return PocketKaiDepartment(**result)

    async def create_or_get_department_by_kai_id(
        self,
        name: str,
        kai_id: int,
    ) -> PocketKaiDepartment:
        try:
            return await self.add_department(name, kai_id)
        except PocketKaiApiError as e:
            if e.status_code == 409:
                return await self.get_department_by_kai_id(kai_id)
            raise e

    async def get_teacher_by_login(self, login: str) -> PocketKaiTeacher | None:
        url = self.base_pocket_kai_url + f'/teacher/by_login/{login}'
        result = await self._json_request('get', url)
        return PocketKaiTeacher(**result) if result else None

    async def add_teacher(
        self,
        login: str,
        name: str,
    ) -> PocketKaiTeacher:
        url = self.base_pocket_kai_url + '/teacher'
        data = {
            'login': login,
            'name': name,
        }
        result = await self._json_request('post', url, json=data)
        return PocketKaiTeacher(**result)

    async def create_or_get_teacher_by_login(
        self,
        login: str,
        name: str,
    ) -> PocketKaiTeacher:
        try:
            return await self.add_teacher(login, name)
        except PocketKaiApiError as e:
            if e.status_code == 409:
                return await self.get_teacher_by_login(login)
            raise e

    async def add_group_lesson(
        self,
        number_of_day: int,
        original_dates: str | None,
        parsed_parity: WeekParity,
        parsed_dates: list[datetime.date] | None,
        parsed_dates_status: ParsedDatesStatus,
        audience_number: str | None,
        building_number: str | None,
        original_lesson_type: str | None,
        parsed_lesson_type: str | None,
        start_time: datetime.time,
        end_time: datetime.time | None,
        discipline_id: UUID,
        teacher_id: UUID | None,
        department_id: UUID | None,
        group_id: UUID,
    ) -> PocketKaiLesson:
        url = self.base_pocket_kai_url + '/lesson'
        data = {
            'number_of_day': number_of_day,
            'original_dates': original_dates,
            'parsed_parity': parsed_parity,
            'parsed_dates': [date.isoformat() for date in parsed_dates]
            if parsed_dates
            else None,
            'parsed_dates_status': parsed_dates_status,
            'audience_number': audience_number,
            'building_number': building_number,
            'original_lesson_type': original_lesson_type,
            'parsed_lesson_type': parsed_lesson_type,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat() if end_time else None,
            'discipline_id': str(discipline_id),
            'teacher_id': str(teacher_id) if teacher_id else None,
            'department_id': str(department_id) if department_id else None,
            'group_id': str(group_id),
        }
        result = await self._json_request('post', url, json=data)
        return PocketKaiLesson(**result)

    async def update_group_lesson(
        self,
        lesson_id: UUID,
        number_of_day: int,
        original_dates: str | None,
        parsed_parity: WeekParity,
        parsed_dates: list[datetime.date] | None,
        parsed_dates_status: ParsedDatesStatus,
        audience_number: str | None,
        building_number: str | None,
        original_lesson_type: str | None,
        parsed_lesson_type: str | None,
        start_time: datetime.time,
        end_time: datetime.time | None,
        discipline_id: UUID,
        teacher_id: UUID | None,
        department_id: UUID | None,
        group_id: UUID,
    ) -> PocketKaiLesson:
        url = self.base_pocket_kai_url + f'/lesson/{lesson_id}'
        data = {
            'number_of_day': number_of_day,
            'original_dates': original_dates,
            'parsed_parity': parsed_parity,
            'parsed_dates': [date.isoformat() for date in parsed_dates]
            if parsed_dates
            else None,
            'parsed_dates_status': parsed_dates_status,
            'audience_number': audience_number,
            'building_number': building_number,
            'original_lesson_type': original_lesson_type,
            'parsed_lesson_type': parsed_lesson_type,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat() if end_time else None,
            'discipline_id': str(discipline_id),
            'teacher_id': str(teacher_id) if teacher_id else None,
            'department_id': str(department_id) if department_id else None,
            'group_id': str(group_id),
        }
        result = await self._json_request('put', url, json=data)
        return PocketKaiLesson(**result)

    async def delete_group_lesson(self, lesson_id: UUID) -> None:
        url = self.base_pocket_kai_url + f'/lesson/{lesson_id}'
        await self._json_request('delete', url)

    async def _get_groups(self, limit: int, offset: int) -> list[PocketKaiGroup]:
        url = self.base_pocket_kai_url + '/group/'
        params = {
            'limit': limit,
            'offset': offset,
            'is_short': 'false',
        }
        result = await self._json_request('get', url, params=params)
        return [PocketKaiGroup(**group_dict) for group_dict in result]

    async def get_all_groups(self) -> list[PocketKaiGroup]:
        all_groups = list()
        limit = 100
        offset = 0
        while groups := await self._get_groups(limit=limit, offset=offset):
            all_groups.extend(groups)
            offset += limit

        return all_groups
