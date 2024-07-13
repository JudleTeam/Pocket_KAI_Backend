from uuid import UUID

from datetime import date

from core.entities.base import BaseEntity


class KaiUserEntity(BaseEntity):
    kai_id: int | None
    position: int | None
    login: str | None
    password: str | None
    full_name: str
    phone: str | None
    email: str
    sex: str | None
    birthday: date | None
    is_leader: bool
    zach_number: str | None
    competition_type: str | None
    contract_number: str | None
    edu_level: str | None
    edu_cycle: str | None
    edu_qualification: str | None
    program_form: str | None
    status: str | None

    group_id: UUID
    pocket_kai_user_id: UUID | None
