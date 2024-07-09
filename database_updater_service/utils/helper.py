from typing import Any

from utils.kai_parser_api.schemas import ParsedLesson
from utils.pocket_kai_api.schemas import PocketKaiLesson


def lesson_key(lesson: ParsedLesson) -> tuple:
    return (
        lesson.day_number,
        lesson.start_time,
        lesson.end_time,
        lesson.dates,
        tuple(lesson.parsed_dates) if lesson.parsed_dates else None,
        lesson.parsed_dates_status,
        lesson.parsed_parity,
        lesson.parsed_lesson_type,
        lesson.discipline_type,
        lesson.discipline_number,
        lesson.audience_number,
        lesson.building_number,
        lesson.department_id,
        lesson.teacher_login or None,
    )


def pocket_lesson_key(lesson: PocketKaiLesson) -> tuple:
    return (
        lesson.number_of_day,
        lesson.start_time,
        lesson.end_time,
        lesson.original_dates,
        tuple(lesson.parsed_dates) if lesson.parsed_dates else None,
        lesson.parsed_dates_status,
        lesson.parsed_parity,
        lesson.parsed_lesson_type,
        lesson.original_lesson_type,
        lesson.discipline.kai_id,
        lesson.audience_number,
        lesson.building_number,
        lesson.department.kai_id if lesson.department else None,
        lesson.teacher.login if lesson.teacher else None,
    )


def compare_lessons(parsed: ParsedLesson, pocket: PocketKaiLesson) -> dict[str, Any]:
    differences = {}

    if parsed.day_number != pocket.number_of_day:
        differences['day_number'] = (parsed.day_number, pocket.number_of_day)
    if parsed.start_time != pocket.start_time:
        differences['start_time'] = (parsed.start_time, pocket.start_time)
    if parsed.end_time != pocket.end_time:
        differences['end_time'] = (parsed.end_time, pocket.end_time)
    if parsed.dates != pocket.original_dates:
        differences['dates'] = (parsed.dates, pocket.original_dates)
    if parsed.parsed_dates != pocket.parsed_dates:
        differences['parsed_dates'] = (parsed.parsed_dates, pocket.parsed_dates)
    if parsed.parsed_parity != pocket.parsed_parity:
        differences['parsed_parity'] = (parsed.parsed_parity, pocket.parsed_parity)
    if parsed.parsed_dates_status != pocket.parsed_dates_status:
        differences['parsed_dates_status'] = (
            parsed.parsed_dates_status,
            pocket.parsed_dates_status,
        )
    if parsed.parsed_lesson_type != pocket.parsed_lesson_type:
        differences['parsed_lesson_type'] = (
            parsed.parsed_lesson_type,
            pocket.parsed_lesson_type,
        )
    if parsed.audience_number != pocket.audience_number:
        differences['audience_number'] = (
            parsed.audience_number,
            pocket.audience_number,
        )
    if parsed.building_number != pocket.building_number:
        differences['building_number'] = (
            parsed.building_number,
            pocket.building_number,
        )
    # if parsed.teacher_name != (pocket.teacher.name if pocket.teacher else None):
    #     differences['teacher_name'] = (parsed.teacher_name, (pocket.teacher.name if pocket.teacher else None))
    if parsed.teacher_login != (pocket.teacher.login if pocket.teacher else None):
        differences['teacher_login'] = (
            parsed.teacher_login,
            (pocket.teacher.name if pocket.teacher else None),
        )
    if parsed.department_id != (
        pocket.department.kai_id if pocket.department else None
    ):
        differences['department_id'] = (
            parsed.department_id,
            (pocket.department.kai_id if pocket.department else None),
        )

    for diff in differences:
        differences[diff] = {
            'before': differences[diff][0],
            'after': differences[diff][1],
        }

    return differences


def find_changes_in_lessons(
    parsed_lessons: list[ParsedLesson],
    pocket_kai_lessons: list[PocketKaiLesson],
):
    parsed_lessons_dict = {lesson_key(lesson): lesson for lesson in parsed_lessons}
    pocket_lessons_dict = {
        pocket_lesson_key(lesson): lesson for lesson in pocket_kai_lessons
    }

    unchanged_lessons = list()
    changed_lessons = list()

    for key in list(parsed_lessons_dict.keys()):
        if key in pocket_lessons_dict:
            parsed_lessons_dict.pop(key)
            pocket_lesson = pocket_lessons_dict.pop(key)
            unchanged_lessons.append(pocket_lesson)

    for parsed_lesson_key, parsed_lesson in parsed_lessons_dict.copy().items():
        possible_pairs = list()
        for (
            pocket_kai_lesson_key,
            pocket_kai_lesson,
        ) in pocket_lessons_dict.copy().items():
            if (
                parsed_lesson.discipline_number == pocket_kai_lesson.discipline.kai_id
                and parsed_lesson.discipline_type
                == pocket_kai_lesson.original_lesson_type
            ):
                possible_pairs.append((pocket_kai_lesson_key, pocket_kai_lesson))

        if len(possible_pairs) >= 1:
            # Подбирает новому уроку пару с наименьшей разницей
            differences = [
                compare_lessons(parsed_lesson, possible_pair[1])
                for possible_pair in possible_pairs
            ]
            min_diff = min(differences, key=len)
            min_diff_possible_pair = possible_pairs[differences.index(min_diff)]

            changed_lessons.append(
                {
                    'old': min_diff_possible_pair[1],
                    'new': parsed_lesson,
                    'differences': min_diff,
                },
            )

            pocket_lessons_dict.pop(min_diff_possible_pair[0])
            parsed_lessons_dict.pop(parsed_lesson_key)

    lessons_to_delete = list(pocket_lessons_dict.values())
    lessons_to_add = list(parsed_lessons_dict.values())

    return unchanged_lessons, changed_lessons, lessons_to_add, lessons_to_delete
