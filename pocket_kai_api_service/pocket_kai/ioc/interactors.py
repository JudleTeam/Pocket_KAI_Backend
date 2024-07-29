from dishka import Provider, Scope, provide, provide_all

from pocket_kai.application.interactors.department import (
    CreateDepartmentInteractor,
    GetDepartmentByKaiIdInteractor,
)
from pocket_kai.application.interactors.discipline import (
    CreateDisciplineInteractor,
    GetDisciplineByKaiIdInteractor,
)
from pocket_kai.application.interactors.exam import (
    CreateExamInteractor,
    GetExamsByGroupIdInteractor,
    UpdateExamInteractor,
)
from pocket_kai.application.interactors.group import (
    CreateGroupInteractor,
    GetAllGroupsInteractor,
    GetGroupByIdInteractor,
    GetGroupByNameInteractor,
    GroupExtendedDTOConverter,
    PatchGroupByIdInteractor,
    PatchGroupByNameInteractor,
    SuggestGroupsByNameInteractor,
)
from pocket_kai.application.interactors.kai_login import KaiLoginInteractor
from pocket_kai.application.interactors.lesson import (
    CreateLessonInteractor,
    DeleteLessonInteractor,
    ExtendedLessonConverter,
    GetLessonsByGroupIdInteractor,
    UpdateLessonInteractor,
)
from pocket_kai.application.interactors.refresh_token import RefreshTokenPairInteractor
from pocket_kai.application.interactors.schedule import (
    GetDatesScheduleByGroupIdInteractor,
    GetDatesScheduleByGroupNameInteractor,
    GetWeekScheduleByGroupIdInteractor,
    GetWeekScheduleByGroupNameInteractor,
)
from pocket_kai.application.interactors.service_token import CheckServiceTokenInteractor
from pocket_kai.application.interactors.student import (
    AddGroupMembersInteractor,
    GetStudentByUserIdInteractor,
)
from pocket_kai.application.interactors.task import GetTasksInteractor
from pocket_kai.application.interactors.teacher import (
    CreateTeacherInteractor,
    GetTeacherByLoginInteractor,
)
from pocket_kai.application.interactors.user import GetUserByAccessTokenInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    group_extended_dto_converter = provide(
        GroupExtendedDTOConverter,
    )

    extended_lesson_converter = provide(
        ExtendedLessonConverter,
    )

    interactors = provide_all(
        CheckServiceTokenInteractor,
        GetTeacherByLoginInteractor,
        CreateTeacherInteractor,
        GetDepartmentByKaiIdInteractor,
        CreateDepartmentInteractor,
        GetDisciplineByKaiIdInteractor,
        CreateDisciplineInteractor,
        SuggestGroupsByNameInteractor,
        GetAllGroupsInteractor,
        GetGroupByNameInteractor,
        GetGroupByIdInteractor,
        CreateGroupInteractor,
        PatchGroupByNameInteractor,
        PatchGroupByIdInteractor,
        KaiLoginInteractor,
        GetLessonsByGroupIdInteractor,
        CreateLessonInteractor,
        DeleteLessonInteractor,
        UpdateLessonInteractor,
        RefreshTokenPairInteractor,
        GetWeekScheduleByGroupNameInteractor,
        GetWeekScheduleByGroupIdInteractor,
        GetDatesScheduleByGroupNameInteractor,
        GetDatesScheduleByGroupIdInteractor,
        AddGroupMembersInteractor,
        GetStudentByUserIdInteractor,
        GetUserByAccessTokenInteractor,
        GetTasksInteractor,
        CreateExamInteractor,
        GetExamsByGroupIdInteractor,
        UpdateExamInteractor,
        scope=Scope.REQUEST,
    )
