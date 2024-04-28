class PocketKaiService:
    host = 'http://pocket_kai_fastapi:8000/'

    @classmethod
    async def get_group_schedule(self, group_id: int) -> list:
        url = self.host + 'schedule/group/' + str(group_id)



