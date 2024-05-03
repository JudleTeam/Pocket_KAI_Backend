import asyncio
from pprint import pprint


from utils.kai_parser.parser import KaiParser
from database.models.kai import GroupLesson


def lesson_type_to_emoji(lesson_type: str):
    lessons_emoji = {
        'лек': '📢',
        'пр': '📝',
        'л.р.': '🧪',
        'физ': '🏆',
        'конс': '❓',
        'к.р.': '🎓',
        'и.з.': '🎯'
    }

    return lessons_emoji.get(lesson_type, lesson_type)


def lesson_type_to_text(lesson_type: str):
    lessons_text = {
        'лек':  'Лекция',
        'пр':   'Практика',
        'л.р.': 'Лаб. раб.',
        'физ':  'Физ-ра',
        'конс': 'Конс.',
        'к.р.': 'Курс. раб.',
        'и.з.': 'Инд. зад.'
    }

    return lessons_text.get(lesson_type, lesson_type)


async def get_schedule_by_week_day(group_id: int, day_of_week: int, parity: int, db):
    async with db.begin() as session:
        schedule = await GroupLesson.get_group_day_schedule(session, group_id, day_of_week)

        if not schedule:  # free day
            return None

        schedule = [schedule_item for schedule_item in schedule if schedule_item.parsed_parity in (0, parity)]
        schedule = sorted(schedule, key=lambda x: x.start_time)

        return schedule


async def main():
    k = KaiParser()
    groups = await k.get_group_ids()
    possible_parity = set()
    total = len(groups)
    for num, group in enumerate(groups[:2], start=1):
        schedule = await k.get_group_schedule(group.id)  # 23551 - 4120

        pprint(schedule)
        print(f'{num}/{total}')
        # pprint(schedule)
        # print()

    pprint(possible_parity)


if __name__ == '__main__':
    asyncio.run(main())
