from datetime import datetime

from bs4 import BeautifulSoup

from utils.kai_parser.schemas.group import Documents, Group
from utils.kai_parser.schemas.user import BaseUser, UserInfo
from utils.kai_parser.utils import parse_phone_number


def parse_user_info(soup: BeautifulSoup):
    last_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_lastName')['value'].strip()
    first_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_firstName')['value'].strip()
    middle_name = soup.find('input', id='_aboutMe_WAR_aboutMe10_middleName')['value'].strip()

    full_name = ' '.join((last_name, first_name, middle_name))

    sex = ''
    sex_select = soup.find('select', id='_aboutMe_WAR_aboutMe10_sex')
    for option in sex_select.findAll():
        if option.get('selected') is not None:
            sex = option.text.strip()
            break

    birthday_str = soup.find('input', id='_aboutMe_WAR_aboutMe10_birthDay')['value'].strip()
    birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()

    phone = soup.find('input', id='_aboutMe_WAR_aboutMe10_phoneNumber0')['value'].strip()
    phone = parse_phone_number(phone)

    email = soup.find('input', id='_aboutMe_WAR_aboutMe10_email')['value'].strip().lower()

    user_info = UserInfo(
        full_name=full_name,
        sex=sex,
        birthday=birthday,
        phone=phone,
        email=email
    )

    return user_info


def parse_group_members(soup: BeautifulSoup) -> Group:
    group_members = list()
    leader_num = None
    last_table = soup.find_all('table')[-1]
    table_rows = last_table.find_all('tr')
    for num, row in enumerate(table_rows[1:], start=1):
        columns = row.find_all('td')

        full_name = columns[1].text.strip()
        if 'Староста' in full_name:
            leader_num = num
            full_name = full_name.replace('Староста', '').strip()
        email = columns[2].text.strip().lower()
        phone = parse_phone_number(columns[3].text.strip())

        user = BaseUser(full_name=full_name, email=email, phone=phone)
        group_members.append(user)

    return Group(members=group_members, leader_num=leader_num)


def parse_documents(soup: BeautifulSoup) -> Documents:
    content = soup.find('div', class_='row div_container')

    def check_edu(text):
        if text is None or text.name != 'a':
            return False
        return 'Образовательная программа' in text

    def check_syllabus(text):
        if text is None or text.name != 'a':
            return False
        return 'Учебный план' in text

    def check_schedule(text):
        if text is None or text.name != 'a':
            return False
        return 'Календарный график' in text

    edu_program_raw = content.find(name=check_edu)
    syllabus_raw = content.find(name='a', string=check_syllabus)
    study_schedule_raw = content.find(name='a', string=check_schedule)

    return Documents(
        syllabus=syllabus_raw['href'] if syllabus_raw else None,
        educational_program=edu_program_raw['href'] if edu_program_raw else None,
        study_schedule=study_schedule_raw['href'] if study_schedule_raw else None
    )
