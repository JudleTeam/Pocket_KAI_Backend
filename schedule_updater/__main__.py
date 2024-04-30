import asyncio

from .main import parse_and_save_all_groups_schedule

if __name__ == '__main__':
    asyncio.run(parse_and_save_all_groups_schedule())
