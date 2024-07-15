from uuid import UUID

from api.schemas.student import AddGroupMembersRequest, StudentRead
from core.services.group import GroupServiceBase
from core.services.student import StudentServiceBase
from core.unit_of_work import UnitOfWorkBase


class StudentUseCase:
    def __init__(
        self,
        student_service: StudentServiceBase,
        group_service: GroupServiceBase,
        uow: UnitOfWorkBase,
    ):
        self.student_service = student_service
        self.group_service = group_service
        self.uow = uow

    async def get_by_user_id(self, user_id: UUID) -> StudentRead:
        student = await self.student_service.get_by_user_id(user_id=user_id)
        return StudentRead.model_validate(student)

    async def add_group_members(
        self,
        add_group_members_request: AddGroupMembersRequest,
    ) -> list[StudentRead]:
        group = await self.group_service.get_by_name(
            group_name=add_group_members_request.group_name,
        )

        added_students = list()
        existing_students = await self.student_service.get_by_group_id(
            group_id=group.id,
        )
        for new_student in add_group_members_request.students:
            for existing_student in existing_students:
                # Если новый студент уже существует, то обновляем его
                if existing_student.email == new_student.email:
                    existing_student.full_name = new_student.full_name
                    existing_student.position = new_student.number
                    existing_student.is_leader = new_student.is_leader
                    existing_student.phone = new_student.phone
                    current_student = await self.student_service.update(
                        existing_student,
                    )
                    added_students.append(current_student)

                    existing_students.remove(existing_student)
                    break

            else:  # Новый студент
                current_student = await self.student_service.create(
                    position=new_student.number,
                    full_name=new_student.full_name,
                    phone=new_student.phone,
                    email=new_student.email,
                    is_leader=new_student.is_leader,
                    group_id=group.id,
                )
                added_students.append(current_student)

                if new_student.is_leader:
                    group.group_leader_id = current_student.id
                    group = await self.group_service.update(group)

        # Оставшиеся в списке студенты лишние, открепляем их от группы
        for student_to_unlink in existing_students:
            student_to_unlink.group_id = None
            student_to_unlink.position = None
            student_to_unlink.is_leader = False
            await self.student_service.update(student_to_unlink)

        await self.uow.commit()

        return [StudentRead.model_validate(student) for student in added_students]
