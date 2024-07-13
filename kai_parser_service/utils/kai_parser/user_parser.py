import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiohttp import ClientError, ClientResponse, ClientSession
from bs4 import BeautifulSoup

from utils.kai_parser import helper
from utils.kai_parser.schemas.errors import KaiApiError
from utils.kai_parser.schemas.group import Documents
from utils.kai_parser.schemas.user import GroupMember, UserAbout, UserInfo


class RetryError(Exception):
    pass


class KaiUserParser:
    kai_main_url = 'https://kai.ru/main'
    about_me_url = 'https://kai.ru/group/guest/common/about-me'
    my_group_url = 'https://kai.ru/group/guest/student/moa-gruppa'
    syllabus_url = 'https://kai.ru/group/guest/student/ucebnyj-plan'

    def __init__(self, session: ClientSession, timeout=30, max_retries=3):
        self.login = None
        self.logged_in = False

        self.session = session
        self.max_retries = max_retries
        self.timeout = timeout

    @property
    def cookies(self):
        return self.session.cookie_jar.filter_cookies(self.kai_main_url)

    @cookies.setter
    def cookies(self, value):
        self.session.cookie_jar.update_cookies(value)

    @asynccontextmanager
    async def _request(
        self,
        method,
        url,
        *,
        current_retry=0,
        **kwargs,
    ) -> AsyncIterator[ClientResponse]:
        try:
            async with self.session.request(
                method=method,
                url=url,
                **kwargs,
                timeout=self.timeout,
            ) as response:
                if not response.ok:
                    raise RetryError
                yield response

        except (asyncio.TimeoutError, ClientError, RetryError):
            if current_retry < self.max_retries:
                async with self._request(
                    method,
                    url,
                    current_retry=current_retry + 1,
                    **kwargs,
                ) as response:
                    yield response
            raise KaiApiError(f'URL: {url} | Status: {response.status}')

    async def _awaitable_request(self, **kwargs):
        async with self._request(**kwargs) as response:
            return response

    async def kai_login(self, login, password):
        cookies = {
            'COOKIE_SUPPORT': 'true',
            'GUEST_LANGUAGE_ID': 'ru_RU',
        }
        self.session.cookie_jar.update_cookies(cookies)
        # Проставляем куки, чтобы можно было залогиниться

        login_data = {
            '_58_login': login,
            '_58_password': password,
        }
        login_params = {
            'p_p_id': 58,
            'p_p_lifecycle': 1,
            'p_p_state': 'minimized',
            '_58_struts_action': '/login/login',
        }

        await self._awaitable_request(
            method='POST',
            url=self.kai_main_url,
            data=login_data,
            params=login_params,
        )

        for el in self.session.cookie_jar:
            # Этот cookie проставляется, когда логин успешный
            if el.key == 'USER_UUID':
                self.logged_in = True
                self.login = login
                return True

        return False

    async def get_user_about(self) -> UserAbout | None:
        if not self.logged_in:
            return

        request_params = {
            'p_p_id': 'aboutMe_WAR_aboutMe10',
            'p_p_lifecycle': 2,
            'p_p_state': 'minimized',
            'p_p_resource_id': 'getRoleData',
            'p_p_cacheability': 'cacheLevelPage',
            'p_p_col_id': 'column-2',
            'p_p_col_count': 1,
        }
        about_me_data = {
            'login': self.login,
            'tab': 'student',
        }

        async with self._request(
            'POST',
            self.about_me_url,
            data=about_me_data,
            params=request_params,
        ) as response:
            user_data_dict = await response.json(content_type='text/html')

        for user_about in user_data_dict['list']:
            if (
                user_about['status'].strip().lower() == 'студент'
                or user_about['tabName'].strip().lower() == 'студент'
            ):
                return UserAbout.model_validate(user_about)

        return None

    async def get_user_info(self) -> UserInfo:
        """
        Обязательно должно быть вызвано перед get_user_about! После выполнения get_user_about выдаст ошибку
        :return:
        """
        if not self.logged_in:
            return

        async with self._request('GET', url=self.about_me_url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

        return helper.parse_user_info(soup)

    async def get_user_group_members(
        self,
        group_name: str | None = None,
    ) -> list[GroupMember]:
        async with self._request('GET', self.my_group_url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

        return helper.parse_group_members(soup, group_name=group_name)

    async def get_documents(self) -> Documents:
        """Need fix"""
        async with self._request('GET', self.syllabus_url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

        return helper.parse_documents(soup)
