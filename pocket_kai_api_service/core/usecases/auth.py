from core.exceptions.base import EntityNotFoundError
from core.security.jwt import JWTManagerProtocol
from core.services.group import GroupServiceBase
from core.services.refresh_token import RefreshTokenServiceBase
from core.services.student import StudentServiceBase
from core.services.user import UserServiceBase
from core.unit_of_work import UnitOfWorkBase
from utils.kai_parser_api.api import KaiParserApi


class AuthUseCase:
    def __init__(
        self,
        student_service: StudentServiceBase,
        group_service: GroupServiceBase,
        user_service: UserServiceBase,
        refresh_token_service: RefreshTokenServiceBase,
        kai_parser_api: KaiParserApi,
        jwt_manager: JWTManagerProtocol,
        uow: UnitOfWorkBase,
    ):
        self.student_service = student_service
        self.group_service = group_service
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service
        self.kai_parser_api = kai_parser_api
        self.jwt_manager = jwt_manager
        self.uow = uow

    async def login_by_kai(self, username: str, password: str) -> tuple[str, str]:
        username = username.lower()

        user_about, user_info = await self.kai_parser_api.kai_login(username, password)

        group = await self.group_service.add_additional_data_from_user_about(
            group_name=str(user_about.groupNum),
            user_about=user_about,
        )

        try:
            student = await self.student_service.get_by_email(email=user_info.email)
        except EntityNotFoundError:
            student = await self.student_service.create(
                kai_id=user_about.studId,
                login=username,
                password=password,
                full_name=user_info.full_name,
                phone=user_info.phone,
                email=user_info.email,
                sex=user_info.sex,
                birthday=user_info.birthday,
                zach_number=user_about.zach,
                competition_type=user_about.competitionType,
                contract_number=user_about.numDog,
                edu_level=user_about.eduLevel,
                edu_cycle=user_about.eduCycle,
                edu_qualification=user_about.eduQualif,
                program_form=user_about.programForm,
                status=user_about.status,
                group_id=group.id,
            )
        else:
            student.kai_id = user_about.studId
            student.login = username
            student.password = password
            student.full_name = user_info.full_name
            student.phone = user_info.phone
            student.sex = user_info.sex
            student.birthday = user_info.birthday
            student.zach_number = user_about.zach
            student.competition_type = user_about.competitionType
            student.contract_number = user_about.numDog
            student.edu_level = user_about.eduLevel
            student.edu_cycle = user_about.eduCycle
            student.edu_qualification = user_about.eduQualif
            student.program_form = user_about.programForm
            student.status = user_about.status
            student.group_id = group.id

            student = await self.student_service.update(student)

        if student.user_id is None:
            user = await self.user_service.create()
            student.user_id = user.id
            await self.student_service.update(student)
        else:
            user = await self.user_service.get_by_id(student.user_id)

        access_token = self.jwt_manager.create_access_token(user_id=str(user.id))
        refresh_token = await self.refresh_token_service.issue_new_token(
            user_id=user.id,
        )

        await self.uow.commit()

        return access_token, refresh_token.token

    async def refresh_token_pair(self, refresh_token: str) -> tuple[str, str]:
        refresh_token = await self.refresh_token_service.refresh_token(
            refresh_token=refresh_token,
        )
        user = await self.user_service.get_by_id(refresh_token.user_id)
        new_access_token = self.jwt_manager.create_access_token(user_id=str(user.id))

        await self.uow.commit()

        return new_access_token, refresh_token.token
