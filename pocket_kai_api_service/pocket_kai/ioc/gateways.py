from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.department import (
    DepartmentGatewayProtocol,
    DepartmentReader,
    DepartmentSaver,
)
from pocket_kai.application.interfaces.entities.discipline import (
    DisciplineGatewayProtocol,
    DisciplineReader,
    DisciplineSaver,
)
from pocket_kai.application.interfaces.entities.exam import (
    ExamDeleter,
    ExamGatewayProtocol,
    ExamReader,
    ExamSaver,
    ExamUpdater,
)
from pocket_kai.application.interfaces.entities.group import (
    GroupGatewayProtocol,
    GroupReader,
    GroupSaver,
    GroupUpdater,
)
from pocket_kai.application.interfaces.entities.institute import (
    InstituteGatewayProtocol,
    InstituteReader,
    InstituteSaver,
)
from pocket_kai.application.interfaces.entities.lesson import (
    LessonDeleter,
    LessonGatewayProtocol,
    LessonReader,
    LessonSaver,
    LessonUpdater,
)
from pocket_kai.application.interfaces.entities.profile import (
    ProfileGatewayProtocol,
    ProfileReader,
    ProfileSaver,
)
from pocket_kai.application.interfaces.entities.refresh_token import (
    RefreshTokenGatewayProtocol,
    RefreshTokenReader,
    RefreshTokenSaver,
    RefreshTokenUpdater,
)
from pocket_kai.application.interfaces.entities.service_token import ServiceTokenReader
from pocket_kai.application.interfaces.entities.speciality import (
    SpecialityGatewayProtocol,
    SpecialityReader,
    SpecialitySaver,
)
from pocket_kai.application.interfaces.entities.student import (
    StudentGatewayProtocol,
    StudentReader,
    StudentSaver,
    StudentUpdater,
)
from pocket_kai.application.interfaces.entities.task import TaskReader
from pocket_kai.application.interfaces.entities.teacher import (
    TeacherReader,
    TeacherSaver,
)
from pocket_kai.application.interfaces.entities.user import UserReader, UserSaver
from pocket_kai.config import Settings
from pocket_kai.infrastructure.gateways.department import DepartmentGateway
from pocket_kai.infrastructure.gateways.discipline import DisciplineGateway
from pocket_kai.infrastructure.gateways.exam import ExamGateway
from pocket_kai.infrastructure.gateways.group import GroupGateway
from pocket_kai.infrastructure.gateways.institute import InstituteGateway
from pocket_kai.infrastructure.gateways.lesson import LessonGateway
from pocket_kai.infrastructure.gateways.profile import ProfileGateway
from pocket_kai.infrastructure.gateways.refresh_token import RefreshTokenGateway
from pocket_kai.infrastructure.gateways.service_token import ServiceTokenGateway
from pocket_kai.infrastructure.gateways.speciality import SpecialityGateway
from pocket_kai.infrastructure.gateways.student import StudentGateway
from pocket_kai.infrastructure.gateways.task import TaskGateway
from pocket_kai.infrastructure.gateways.teacher import TeacherGateway
from pocket_kai.infrastructure.gateways.user import UserGateway


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_teacher_gateway(
        self,
        session: AsyncSession,
        config: Settings,
    ) -> AnyOf[TeacherReader, TeacherSaver]:
        return TeacherGateway(
            session=session,
            search_similarity_threshold=config.common.TEACHER_SEARCH_SIMILARITY,
        )

    service_token_gateway = provide(
        ServiceTokenGateway,
        provides=ServiceTokenReader,
    )

    department_gateway = provide(
        DepartmentGateway,
        provides=AnyOf[DepartmentReader, DepartmentSaver, DepartmentGatewayProtocol],
    )

    discipline_gateway = provide(
        DisciplineGateway,
        provides=AnyOf[DisciplineReader, DisciplineSaver, DisciplineGatewayProtocol],
    )

    group_gateway = provide(
        GroupGateway,
        provides=AnyOf[GroupReader, GroupSaver, GroupUpdater, GroupGatewayProtocol],
    )

    institute_gateway = provide(
        InstituteGateway,
        provides=AnyOf[InstituteReader, InstituteSaver, InstituteGatewayProtocol],
    )

    lesson_gateway = provide(
        LessonGateway,
        provides=AnyOf[
            LessonReader,
            LessonSaver,
            LessonUpdater,
            LessonDeleter,
            LessonGatewayProtocol,
        ],
    )

    profile_gateway = provide(
        ProfileGateway,
        provides=AnyOf[ProfileReader, ProfileSaver, ProfileGatewayProtocol],
    )

    refresh_token_gateway = provide(
        RefreshTokenGateway,
        provides=AnyOf[
            RefreshTokenReader,
            RefreshTokenSaver,
            RefreshTokenUpdater,
            RefreshTokenGatewayProtocol,
        ],
    )

    speciality_gateway = provide(
        SpecialityGateway,
        provides=AnyOf[SpecialityReader, SpecialitySaver, SpecialityGatewayProtocol],
    )

    student_gateway = provide(
        StudentGateway,
        provides=AnyOf[
            StudentReader,
            StudentSaver,
            StudentUpdater,
            StudentGatewayProtocol,
        ],
    )

    user_gateway = provide(
        UserGateway,
        provides=AnyOf[UserReader, UserSaver],
    )

    task_gateway = provide(
        TaskGateway,
        provides=AnyOf[TaskReader],
    )

    exam_gateway = provide(
        ExamGateway,
        provides=AnyOf[
            ExamSaver,
            ExamReader,
            ExamUpdater,
            ExamDeleter,
            ExamGatewayProtocol,
        ],
    )
