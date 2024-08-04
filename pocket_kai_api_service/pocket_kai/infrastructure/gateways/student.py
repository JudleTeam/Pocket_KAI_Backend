import dataclasses

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.student import (
    StudentReader,
    StudentSaver,
    StudentUpdater,
)
from pocket_kai.domain.entitites.student import StudentEntity
from pocket_kai.domain.exceptions.student import StudentAlreadyExistsError
from pocket_kai.infrastructure.database.models.kai import StudentModel


class StudentGateway(StudentReader, StudentSaver, StudentUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(student_record: StudentModel | None):
        if student_record is None:
            return None

        return StudentEntity(
            id=student_record.id,
            created_at=student_record.created_at,
            kai_id=student_record.kai_id,
            position=student_record.position,
            login=student_record.login,
            password=student_record.password,
            full_name=student_record.full_name,
            phone=student_record.phone,
            email=student_record.email,
            sex=student_record.sex,
            birthday=student_record.birthday,
            is_leader=student_record.is_leader,
            zach_number=student_record.zach_number,
            competition_type=student_record.competition_type,
            contract_number=student_record.contract_number,
            edu_level=student_record.edu_level,
            edu_cycle=student_record.edu_cycle,
            edu_qualification=student_record.edu_qualification,
            program_form=student_record.program_form,
            status=student_record.status,
            group_id=student_record.group_id,
            user_id=student_record.user_id,
        )

    async def get_by_email(self, email: str) -> StudentEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(StudentModel).where(StudentModel.email == email),
            ),
        )

    async def get_by_user_id(self, user_id: str) -> StudentEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(StudentModel).where(StudentModel.user_id == user_id),
            ),
        )

    async def get_by_group_id(self, group_id: str) -> list[StudentEntity]:
        return [
            self._db_to_entity(student_record)
            for student_record in await self._session.scalars(
                select(StudentModel)
                .where(StudentModel.group_id == group_id)
                .order_by(StudentModel.position),
            )
        ]

    async def save(self, student: StudentEntity) -> None:
        try:
            await self._session.execute(
                insert(StudentModel).values(**dataclasses.asdict(student)),
            )
        except IntegrityError:
            raise StudentAlreadyExistsError

    async def update(self, student: StudentEntity) -> None:
        update_dict = dataclasses.asdict(student)
        update_dict.pop('id')

        try:
            await self._session.execute(
                update(StudentModel)
                .where(StudentModel.id == student.id)
                .values(**update_dict),
            )
        except Exception:
            # TODO: Добавить правильные ошибки
            raise
