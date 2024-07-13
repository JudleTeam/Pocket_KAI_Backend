from aiohttp import ClientSession


class PocketKaiApi:
    def __init__(self, base_url: str, session: ClientSession):
        self.base_url = base_url
        self.session = session

    async def send_user_data(self):
        pass
