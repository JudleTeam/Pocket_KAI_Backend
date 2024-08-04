from pocket_kai.application.dto.student import NewStudentDTO
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.group import GroupGatewayProtocol
from pocket_kai.application.interfaces.entities.student import (
    StudentGatewayProtocol,
    StudentReader,
)
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.student import StudentEntity
from pocket_kai.domain.exceptions.group import GroupNotFoundError
from pocket_kai.domain.exceptions.student import StudentNotFoundError


class AddGroupMembersInteractor:
    def __init__(
        self,
        student_gateway: StudentGatewayProtocol,
        group_gateway: GroupGatewayProtocol,
        uow: UnitOfWork,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
    ):
        self.student_gateway = student_gateway
        self.group_gateway = group_gateway
        self.uow = uow
        self.uuid_generator = uuid_generator
        self.datetime_manager = datetime_manager

    async def __call__(self, group_name: str, members: list[NewStudentDTO]) -> None:
        group = await self.group_gateway.get_by_name(group_name=group_name)
        if group is None:
            raise GroupNotFoundError

        existing_students = await self.student_gateway.get_by_group_id(
            group_id=group.id,
        )
        for group_member in members:
            for existing_student in existing_students:
                # Если новый студент уже существует, то обновляем его
                if existing_student.email == group_member.email:
                    existing_student.full_name = group_member.full_name
                    existing_student.position = group_member.number
                    existing_student.is_leader = group_member.is_leader
                    existing_student.phone = group_member.phone
                    await self.student_gateway.update(existing_student)
                    current_student = existing_student

                    existing_students.remove(existing_student)
                    break

            else:  # Новый студент
                new_student = StudentEntity(
                    id=self.uuid_generator(),
                    created_at=self.datetime_manager.now(),
                    kai_id=None,
                    position=group_member.number,
                    login=None,
                    password=None,
                    full_name=group_member.full_name,
                    phone=group_member.phone,
                    email=group_member.email,
                    sex=None,
                    birthday=None,
                    is_leader=group_member.is_leader,
                    zach_number=None,
                    competition_type=None,
                    contract_number=None,
                    edu_level=None,
                    edu_cycle=None,
                    edu_qualification=None,
                    program_form=None,
                    status=None,
                    group_id=group.id,
                    user_id=None,
                )
                await self.student_gateway.save(new_student)
                current_student = new_student

            # Устанавливаем старосту для группы
            if current_student.is_leader:
                group.group_leader_id = current_student.id
                await self.group_gateway.update(group)

        # Оставшиеся в списке студенты лишние, открепляем их от группы
        for student_to_unlink in existing_students:
            student_to_unlink.group_id = None
            student_to_unlink.position = None
            student_to_unlink.is_leader = False
            await self.student_gateway.update(student_to_unlink)

        await self.uow.commit()


class GetStudentByUserIdInteractor:
    def __init__(
        self,
        student_gateway: StudentReader,
    ):
        self._student_gateway = student_gateway

    async def __call__(self, user_id: str) -> StudentEntity:
        student = await self._student_gateway.get_by_user_id(user_id=user_id)
        if student is None:
            raise StudentNotFoundError
        return student


class GetGroupMembersByUserIdInteractor:
    def __init__(
        self,
        student_gateway: StudentReader,
    ):
        self._student_gateway = student_gateway

    async def __call__(self, user_id: str) -> list[StudentEntity]:
        student = await self._student_gateway.get_by_user_id(user_id=user_id)
        if student is None:
            raise StudentNotFoundError

        return await self._student_gateway.get_by_group_id(
            group_id=student.group_id,
        )
