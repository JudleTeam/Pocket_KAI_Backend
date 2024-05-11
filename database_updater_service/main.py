import asyncio
import logging

from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger
from apscheduler import AsyncScheduler

from config import settings
from utils.schedule_updater import ScheduleUpdater
from utils.kai_parser_api.api import KaiParserApi
from utils.pocket_kai_api.api import PocketKaiApi


async def update_schedule():
    async with ClientSession() as session_1, ClientSession() as session_2:
        logging.info('Creating schedule updater...')
        kai_parser_api = KaiParserApi(
            session=session_1,
            base_kai_parser_url=settings.kai_parser_url
        )
        pocket_kai_api = PocketKaiApi(
            session=session_2,
            base_pocket_kai_url=settings.pocket_kai_api_url,
            service_token=settings.service_token
        )

        schedule_updater = ScheduleUpdater(kai_parser_api, pocket_kai_api)
        logging.info('Schedule updater created! Starting schedule updating...')
        await schedule_updater(split_to_chunks=True)


async def start_schedulers():
    scheduler = AsyncScheduler()

    await scheduler.add_schedule(
        update_schedule,
        CronTrigger(hour=3, minute=0, timezone=settings.timezone),
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await update_schedule()


if __name__ == '__main__':
    asyncio.run(main())
