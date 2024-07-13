from aiohttp import ClientSession

from utils.kai_parser_api.schemas import UserAbout, UserInfo


class KaiParserApi:
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
                raise  # TODO: добавить ошибку
            if not response.ok:
                raise  # TODO: добавить ошибку

            result = await response.json()

        return UserAbout(**result['user_about']), UserInfo(**result['user_info'])
