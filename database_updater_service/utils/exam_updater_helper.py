from typing import Any

from utils.kai_parser_api.schemas import ParsedExam
from utils.pocket_kai_api.schemas import PocketKaiExam


def get_previous_semester(
    academic_year: str,
    academic_year_half: int,
) -> tuple[str, int]:
    if academic_year_half == 2:
        return academic_year, 1

    first_year = int(academic_year.split('-')[0])
    return f'{first_year - 1}-{first_year}', 2


def get_parsed_exam_key(parsed_exam: ParsedExam):
    return (
        parsed_exam.date,
        parsed_exam.parsed_date,
        parsed_exam.time,
        parsed_exam.discipline_number,
        parsed_exam.audience_number,
        parsed_exam.building_number,
        parsed_exam.teacher_login,
    )


def get_pocket_kai_exam_key(pocket_kai_exam: PocketKaiExam):
    return (
        pocket_kai_exam.original_date,
        pocket_kai_exam.parsed_date,
        pocket_kai_exam.time,
        pocket_kai_exam.discipline.kai_id if pocket_kai_exam.discipline else None,
        pocket_kai_exam.audience_number,
        pocket_kai_exam.building_number,
        pocket_kai_exam.teacher.login if pocket_kai_exam.teacher else None,
    )


def compare_exams(parsed: ParsedExam, pocket: PocketKaiExam) -> dict[str, Any]:
    differences = {}

    if parsed.date != pocket.original_date:
        differences['original_date'] = (parsed.date, pocket.original_date)

    if parsed.parsed_date != pocket.parsed_date:
        differences['parsed_date'] = (parsed.parsed_date, pocket.parsed_date)

    if parsed.time != pocket.time:
        differences['time'] = (parsed.time, pocket.time)

    if parsed.discipline_number != pocket.discipline.kai_id:
        differences['discipline_number'] = (
            parsed.discipline_number,
            pocket.discipline.kai_id,
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

    if parsed.teacher_login != pocket.teacher.login if pocket.teacher else None:
        differences['teacher_login'] = (
            parsed.teacher_login,
            pocket.teacher.login if pocket.teacher else None,
        )

    for diff in differences:
        differences[diff] = {
            'before': differences[diff][1],
            'after': differences[diff][0],
        }

    return differences


def find_changes_in_exams(
    parsed_exams: list[ParsedExam],
    pocket_kai_exams: list[PocketKaiExam],
):
    parsed_exams_dict = {get_parsed_exam_key(exam): exam for exam in parsed_exams}
    pocket_exams_dict = {
        get_pocket_kai_exam_key(exam): exam for exam in pocket_kai_exams
    }

    unchanged_exams = list()
    changed_exams = list()

    for key in list(parsed_exams_dict.keys()):
        if key in pocket_exams_dict:
            parsed_exams_dict.pop(key)
            pocket_lesson = pocket_exams_dict.pop(key)
            unchanged_exams.append(pocket_lesson)

    for parsed_exam_key, parsed_exam in parsed_exams_dict.copy().items():
        possible_pairs = list()
        for (
            pocket_kai_exam_key,
            pocket_kai_exam,
        ) in pocket_exams_dict.copy().items():
            if parsed_exam.discipline_number == pocket_kai_exam.discipline.kai_id:
                possible_pairs.append((pocket_kai_exam_key, pocket_kai_exam))

        if len(possible_pairs) == 1:
            # Подбирает новому уроку пару с наименьшей разницей
            differences = [
                compare_exams(parsed_exam, possible_pair[1])
                for possible_pair in possible_pairs
            ]
            min_diff = min(differences, key=len)
            min_diff_possible_pair = possible_pairs[differences.index(min_diff)]

            changed_exams.append(
                {
                    'old': min_diff_possible_pair[1],
                    'new': parsed_exam,
                    'differences': min_diff,
                },
            )

            pocket_exams_dict.pop(min_diff_possible_pair[0])
            parsed_exams_dict.pop(parsed_exam_key)

        exams_to_delete = list(pocket_exams_dict.values())
        exams_to_add = list(parsed_exams_dict.values())

        return unchanged_exams, changed_exams, exams_to_add, exams_to_delete
