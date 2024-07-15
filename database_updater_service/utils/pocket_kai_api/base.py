import datetime
from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from utils.common import ParsedDatesStatus
from utils.kai_parser_api.schemas import WeekParity
from utils.pocket_kai_api.schemas import (
    PocketKaiDepartment,
    PocketKaiDiscipline,
    PocketKaiGroup,
    PocketKaiLesson,
    PocketKaiTeacher,
)


class PocketKaiApiError(Exception):
    def __init__(self, status_code: int, message: str = ''):
        self.status_code = status_code
        super().__init__(message)


class PocketKaiApiBase(Protocol):
    @abstractmethod
    async def get_all_groups(self) -> list[PocketKaiGroup]:
        raise NotImplementedError

    @abstractmethod
    async def add_group(self, group_name: str, group_kai_id: int) -> PocketKaiGroup:
        raise NotImplementedError

    @abstractmethod
    async def patch_group(
        self,
        group_id: UUID,
        schedule_parsed_at: datetime.datetime | None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_group_lessons_by_group_id(
        self,
        group_id: UUID,
    ) -> list[PocketKaiLesson]:
        raise NotImplementedError

    @abstractmethod
    async def get_discipline_by_kai_id(self, kai_id: int) -> PocketKaiDiscipline | None:
        raise NotImplementedError

    @abstractmethod
    async def add_discipline(self, name: str, kai_id: int) -> PocketKaiDiscipline:
        raise NotImplementedError

    @abstractmethod
    async def get_department_by_kai_id(self, kai_id: int) -> PocketKaiDepartment | None:
        raise NotImplementedError

    @abstractmethod
    async def add_department(self, name: str, kai_id: int) -> PocketKaiDepartment:
        raise NotImplementedError

    @abstractmethod
    async def get_teacher_by_login(self, login: str) -> PocketKaiTeacher | None:
        raise NotImplementedError

    @abstractmethod
    async def add_teacher(
        self,
        login: str,
        name: str,
        department_id: UUID,
    ) -> PocketKaiTeacher:
        raise NotImplementedError

    @abstractmethod
    async def create_or_get_discipline_by_kai_id(
        self,
        name: str,
        kai_id: int,
    ) -> PocketKaiDiscipline:
        raise NotImplementedError

    @abstractmethod
    async def create_or_get_department_by_kai_id(
        self,
        name: str,
        kai_id: int,
    ) -> PocketKaiDepartment:
        raise NotImplementedError

    @abstractmethod
    async def create_or_get_teacher_by_login(
        self,
        login: str,
        name: str,
        department_id: UUID,
    ) -> PocketKaiTeacher:
        raise NotImplementedError

    @abstractmethod
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
        department_id: UUID,
        group_id: UUID,
    ) -> PocketKaiLesson:
        raise NotImplementedError

    @abstractmethod
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
        department_id: UUID,
        group_id: UUID,
    ) -> PocketKaiLesson:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_lesson(self, lesson_id: UUID) -> None:
        raise NotImplementedError
