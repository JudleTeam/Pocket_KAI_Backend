from datetime import datetime

from bs4 import BeautifulSoup

from utils.kai_parser.schemas.group import Documents
from utils.kai_parser.schemas.user import GroupMember, UserInfo
from utils.kai_parser.utils import parse_phone_number


def parse_user_info(soup: BeautifulSoup):
    last_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_lastName')[
        'value'
    ].strip()
    first_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_firstName')[
        'value'
    ].strip()
    middle_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_middleName')[
        'value'
    ].strip()

    full_name = ' '.join((last_name, first_name, middle_name))

    sex = ''
    sex_select = soup.find('select', id='_aboutMe_WAR_aboutMe10_sex')
    for option in sex_select.findAll():
        if option.get('selected') is not None:
            sex = option.text.strip()
            break

    birthday_str = soup.find('input', id='_aboutMe_WAR_aboutMe10_birthDay')[
        'value'
    ].strip()
    birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()

    phone = soup.find('input', id='_aboutMe_WAR_aboutMe10_phoneNumber0')[
        'value'
    ].strip()
    phone = parse_phone_number(phone)

    email = (
        soup.find('input', id='_aboutMe_WAR_aboutMe10_email')['value'].strip().lower()
    )

    user_info = UserInfo(
        full_name=full_name,
        sex=sex,
        birthday=birthday,
        phone=phone,
        email=email,
    )

    return user_info


def parse_group_members(
    soup: BeautifulSoup,
    group_name: str | None = None,
) -> list[GroupMember]:
    group_table_index = -1
    if group_name:
        buttons = soup.find_all('label', class_='radio')
        for index, button in enumerate(buttons):
            if group_name in button.text.strip():
                group_table_index = index
                break

    group_members = list()
    last_table = soup.find_all('table')[group_table_index]
    table_rows = last_table.find_all('tr')
    for num, row in enumerate(table_rows[1:], start=1):
        columns = row.find_all('td')

        is_leader = False
        full_name = columns[1].text.strip()
        if 'Староста' in full_name:
            is_leader = True
            full_name = full_name.replace('Староста', '').strip()

        email = columns[2].text.strip().lower()
        phone = parse_phone_number(columns[3].text.strip())

        user = GroupMember(
            is_leader=is_leader,
            number=num,
            full_name=full_name,
            email=email,
            phone=phone,
        )
        group_members.append(user)

    return group_members


def parse_documents(soup: BeautifulSoup) -> Documents:
    content = soup.find('div', class_='row div_container')

    def check_for_text_in_a(text: str):
        def check(tag):
            if tag is None or tag.name != 'a':
                return False
            return text in tag

        return check

    edu_program_raw = content.find(
        name=check_for_text_in_a('Образовательная программа'),
    )
    syllabus_raw = content.find(name=check_for_text_in_a('Учебный план'))
    study_schedule_raw = content.find(name=check_for_text_in_a('Календарный график'))

    return Documents(
        syllabus=syllabus_raw['href'] if syllabus_raw else None,
        educational_program=edu_program_raw['href'] if edu_program_raw else None,
        study_schedule=study_schedule_raw['href'] if study_schedule_raw else None,
    )
