from aiohttp import ClientSession

from pocket_kai.application.interfaces.kai_parser_api import KaiParserApiProtocol
from pocket_kai.domain.exceptions.kai_parser import (
    BadKaiCredentialsError,
    KaiParserApiError,
    KaiParsingError,
)
from pocket_kai.infrastructure.kai_parser_api.schemas import (
    TaskSchema,
    TaskStatus,
    TaskType,
    UserAbout,
    UserInfo,
)


class KaiParserApi(KaiParserApiProtocol):
    def __init__(
        self,
        base_url: str,
        session: ClientSession,
    ):
        self.base_url = base_url
        self.session = session

    async def kai_login(
        self,
        username,
        password,
        parse_user_data=True,
    ) -> tuple[UserAbout, UserInfo]:
        async with self.session.post(
            url=self.base_url + '/user/login',
            data={
                'username': username,
                'password': password,
            },
            params={
                'parse_user_data': str(parse_user_data),
            },
        ) as response:
            if response.status == 401:
                raise BadKaiCredentialsError
            if response.status == 503:
                raise KaiParsingError(await response.text())
            if not response.ok:
                raise KaiParserApiError(
                    f'URL: {response.url} | Method: POST | Status code: {response.status} | Content: {await response.text()}',
                )

            result = await response.json()

        return UserAbout(**result['user_about']), UserInfo(**result['user_info'])

    async def get_tasks(
        self,
        limit: int,
        offset: int,
        group_name: str | None,
        login: str | None,
        type: TaskType | None = None,
        status: TaskStatus | None = None,
    ) -> list[TaskSchema]:
        params = {
            'limit': limit,
            'offset': offset,
        }
        if group_name is not None:
            params['group_name'] = group_name
        if login is not None:
            params['login'] = login
        if type is not None:
            params['type'] = type.value
        if status is not None:
            params['status'] = status.value

        async with self.session.get(
            url=self.base_url + '/task',
            params=params,
        ) as response:
            if not response.ok:
                raise KaiParserApiError(
                    f'URL: {response.url} | Method: GET | Status code: {response.status} | Content: {await response.text()}',
                )

            result = await response.json()

        return [TaskSchema.model_validate(task) for task in result]
