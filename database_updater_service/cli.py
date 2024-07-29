import argparse
import asyncio
import logging

from main import update_exams, update_schedule


async def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('update_schedule', help='Update schedule')
    subparsers.add_parser('update_exams', help='Update exams')

    args = parser.parse_args()
    if args.command == 'update_schedule':
        await update_schedule()
    elif args.command == 'update_exams':
        await update_exams()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
