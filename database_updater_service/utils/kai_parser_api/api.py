from aiohttp import ClientSession

from utils.kai_parser_api.base import KaiParserApiBase
from utils.kai_parser_api.schemas import ParsedGroup, ParsedLesson


class KaiParserApi(KaiParserApiBase):
    def __init__(self, session: ClientSession, base_kai_parser_url: str):
        self.session = session
        self.base_kai_parser_url = base_kai_parser_url

    async def _json_request(self, method: str, url: str, params: dict = None) -> dict:
        async with self.session.request(method, url, params=params) as response:
            return await response.json()

    async def get_groups(self) -> list[ParsedGroup]:
        url = self.base_kai_parser_url + '/group'
        json_response = await self._json_request('GET', url)
        return [ParsedGroup.model_validate(group_dict) for group_dict in json_response]

    async def get_group_schedule(self, group_kai_id: int) -> list[ParsedLesson]:
        json_response = await self._json_request(
            'GET',
            url=self.base_kai_parser_url + '/schedule',
            params={'group_kai_id': group_kai_id}
        )
        return [ParsedLesson.model_validate(lesson_dict) for lesson_dict in json_response]
