from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.department import (
    DepartmentGatewayProtocol,
)
from pocket_kai.application.interfaces.entities.group import GroupGatewayProtocol
from pocket_kai.application.interfaces.entities.institute import (
    InstituteGatewayProtocol,
)
from pocket_kai.application.interfaces.kai_parser_api import KaiParserApiProtocol
from pocket_kai.application.interfaces.entities.profile import ProfileGatewayProtocol
from pocket_kai.application.interfaces.entities.refresh_token import RefreshTokenSaver
from pocket_kai.application.interfaces.jwt import JWTManagerProtocol
from pocket_kai.application.interfaces.entities.speciality import (
    SpecialityGatewayProtocol,
)
from pocket_kai.application.interfaces.entities.student import StudentGatewayProtocol
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.application.interfaces.entities.user import UserSaver
from pocket_kai.domain.entitites.department import DepartmentEntity
from pocket_kai.domain.entitites.group import GroupEntity
from pocket_kai.domain.entitites.institute import InstituteEntity
from pocket_kai.domain.entitites.profile import ProfileEntity
from pocket_kai.domain.entitites.refresh_token import RefreshTokenEntity
from pocket_kai.domain.entitites.speciality import SpecialityEntity
from pocket_kai.domain.entitites.student import StudentEntity
from pocket_kai.domain.entitites.user import UserEntity
from pocket_kai.infrastructure.kai_parser_api.schemas import UserAbout, UserInfo


class KaiLoginInteractor:
    def __init__(
        self,
        user_gateway: UserSaver,
        student_gateway: StudentGatewayProtocol,
        group_gateway: GroupGatewayProtocol,
        refresh_token_gateway: RefreshTokenSaver,
        institute_gateway: InstituteGatewayProtocol,
        department_gateway: DepartmentGatewayProtocol,
        profile_gateway: ProfileGatewayProtocol,
        speciality_gateway: SpecialityGatewayProtocol,
        kai_parser_api: KaiParserApiProtocol,
        jwt_manager: JWTManagerProtocol,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
        uow: UnitOfWork,
    ):
        self.user_gateway = user_gateway
        self.student_gateway = student_gateway
        self.group_gateway = group_gateway
        self.refresh_token_gateway = refresh_token_gateway
        self.institute_gateway = institute_gateway
        self.department_gateway = department_gateway
        self.profile_gateway = profile_gateway
        self.speciality_gateway = speciality_gateway

        self.jwt_manager = jwt_manager
        self.uuid_generator = uuid_generator
        self.datetime_manager = datetime_manager
        self.kai_parser_api = kai_parser_api

        self.uow = uow

    async def _issue_new_refresh_token(self, user_id: str) -> RefreshTokenEntity:
        refresh_token_id = self.uuid_generator()
        refresh_token = self.jwt_manager.create_refresh_token(
            jti=str(refresh_token_id),
            user_id=str(user_id),
        )
        refresh_token_payload = self.jwt_manager.decode_refresh_token(refresh_token)

        refresh_token_entity = RefreshTokenEntity(
            id=refresh_token_id,
            created_at=self.datetime_manager.now(),
            token=refresh_token,
            name=None,
            is_revoked=False,
            last_used_at=None,
            revoked_at=None,
            issued_at=refresh_token_payload.iat.replace(tzinfo=None),
            expires_at=refresh_token_payload.exp.replace(tzinfo=None),
            user_id=user_id,
        )

        await self.refresh_token_gateway.save(refresh_token_entity)

        return refresh_token_entity

    async def _create_or_update_student(
        self,
        username: str,
        password: str,
        group_id: str,
        user_info: UserInfo,
        user_about: UserAbout,
    ) -> StudentEntity:
        student = await self.student_gateway.get_by_email(email=user_info.email)

        if student is None:
            student = StudentEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
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
                group_id=group_id,
                position=None,
                is_leader=False,
                user_id=None,
            )
            await self.student_gateway.save(student)
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
            student.group_id = group_id

            await self.student_gateway.update(student)

        return student

    async def _update_group_from_user_about(
        self,
        group_name: str,
        user_about: UserAbout,
    ) -> GroupEntity:
        group = await self.group_gateway.get_by_name(group_name=group_name)

        speciality = await self.speciality_gateway.get_by_kai_id(
            kai_id=user_about.specId,
        )
        if speciality is None:
            speciality = SpecialityEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
                code=user_about.specCode,
                kai_id=user_about.specId,
                name=user_about.specName,
            )
            await self.speciality_gateway.save(speciality)

        institute = await self.institute_gateway.get_by_kai_id(kai_id=user_about.instId)
        if institute is None:
            institute = InstituteEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
                kai_id=user_about.instId,
                name=user_about.instName,
            )
            await self.institute_gateway.save(institute)

        profile = await self.profile_gateway.get_by_kai_id(kai_id=user_about.profileId)
        if profile is None:
            profile = ProfileEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
                kai_id=user_about.profileId,
                name=user_about.profileName,
            )
            await self.profile_gateway.save(profile)

        department = await self.department_gateway.get_by_kai_id(
            kai_id=user_about.kafId,
        )
        if department is None:
            department = DepartmentEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
                kai_id=user_about.kafId,
                name=user_about.kafName,
            )
            await self.department_gateway.save(department)

        group.institute_id = institute.id
        group.speciality_id = speciality.id
        group.profile_id = profile.id
        group.department_id = department.id
        group.is_verified = True
        group.verified_at = self.datetime_manager.now()
        group.parsed_at = self.datetime_manager.now()

        await self.group_gateway.update(group)

        return group

    async def __call__(self, username: str, password: str) -> tuple[str, str]:
        username = username.lower()

        user_about, user_info = await self.kai_parser_api.kai_login(username, password)

        group = await self._update_group_from_user_about(
            group_name=str(user_about.groupNum),
            user_about=user_about,
        )

        student = await self._create_or_update_student(
            username=username,
            password=password,
            group_id=group.id,
            user_info=user_info,
            user_about=user_about,
        )

        if student.user_id is None:
            user = UserEntity(
                id=self.uuid_generator(),
                created_at=self.datetime_manager.now(),
                telegram_id=None,
                phone=None,
                is_blocked=False,
            )
            await self.user_gateway.save(user)

            user_id = user.id
            student.user_id = user.id
            await self.student_gateway.update(student)
        else:
            user_id = student.user_id

        access_token = self.jwt_manager.create_access_token(user_id=str(user_id))
        refresh_token = await self._issue_new_refresh_token(user_id=user_id)

        await self.uow.commit()

        return access_token, refresh_token.token
