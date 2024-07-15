import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiohttp import ClientError, ClientResponse, ClientSession

from utils.kai_parser.schemas.user import GroupMember


class PocketKaiApiError(Exception):
    pass


class PocketKaiApi:
    def __init__(
        self,
        base_url: str,
        session: ClientSession,
        service_token: str,
        max_retries: int = 3,
    ):
        self.base_url = base_url
        self.session = session
        self.max_retries = max_retries

        self.headers = {
            'x-service-token': service_token,
        }

    @asynccontextmanager
    async def _request(
        self,
        method,
        url,
        *,
        current_retry=0,
        **kwargs,
    ) -> AsyncIterator[ClientResponse]:
        if 'headers' in kwargs:
            kwargs.pop('headers')

        try:
            async with self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs,
            ) as response:
                yield response

        except (asyncio.TimeoutError, ClientError) as e:
            if current_retry < self.max_retries:
                async with self._request(
                    method,
                    url,
                    current_retry=current_retry + 1,
                    **kwargs,
                ) as response:
                    yield response
            raise PocketKaiApiError(f'URL: {url} | Error: {e}')

    async def add_group_members(
        self,
        group_name: str,
        group_members: list[GroupMember],
    ):
        async with self._request(
            method='POST',
            url=self.base_url + '/student/add_group_members',
            json={
                'group_name': group_name,
                'students': [
                    group_member.model_dump() for group_member in group_members
                ],
            },
        ) as response:
            if not response.ok:
                raise PocketKaiApiError(await response.text())

    async def patch_group(self, group_name: str, patch: dict):
        async with self._request(
            method='PATCH',
            url=self.base_url + f'/group/by_name/{group_name}',
            json=patch,
        ) as response:
            if not response.ok:
                raise PocketKaiApiError(await response.text())
