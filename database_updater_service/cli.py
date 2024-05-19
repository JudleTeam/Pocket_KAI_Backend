import argparse
import asyncio
import logging

from main import update_schedule


async def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('update_schedule', help='Update schedule')

    args = parser.parse_args()
    if args.command == 'update_schedule':
        await update_schedule()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
