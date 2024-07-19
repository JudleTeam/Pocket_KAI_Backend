from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from pocket_kai.config import Settings, get_settings
from pocket_kai.controllers.http.routers.main import router
from pocket_kai.ioc.main import providers


tags_metadata = [
    {
        'name': 'Groups',
        'description': (
            'Эндпоинты для работы с группы. '
            'Также есть отдельные категории связанные с группами: `Groups schedule` и `Groups lessons`'
        ),
    },
    {
        'name': 'Groups schedule',
        'description': 'Эндпоинты для работы с расписанием групп',
    },
    {
        'name': 'Groups lessons',
        'description': 'Эндпоинты для работы с занятиями групп',
    },
    {
        'name': 'Teachers',
        'description': 'Эндпоинты для работы с преподавателями',
    },
    {
        'name': 'Departments',
        'description': 'Эндпоинты для работы с кафедрами',
    },
    {
        'name': 'Disciplines',
        'description': 'Эндпоинты для работы с дисциплинами',
    },
    {
        'name': 'Lessons',
        'description': (
            'Эндпоинты для работы с занятиями.\n\n'
            '**Parsed dates status** - Статус спаршенных дат. Может быть `good` или `need_check`.\n'
            '`good` - даты получилось распарсить точно, таким датам можно доверять.\n'
            '`need_check` - даты либо не получилось распарсить; либо получилось, но неточно; '
            'либо даты разделены на подгруппы. Такие даты конечному пользователю следует перепроверить самому.\n\n'
            '**! Даты распаршиваются в `parsed_dates` и `parsed_parity` !**'
        ),
    },
]

description = """
Pocket KAI API

## Сервисные токены
Сервисные токены нужны для доступа к **служебным** эндпоинтам. Такие токены выпускаются только админами.
"""

settings = get_settings()
container = make_async_container(
    *providers,
    context={Settings: settings},
)

app = FastAPI(
    title='Pocket KAI API',
    description=description,
    openapi_tags=tags_metadata,
    default_response_class=ORJSONResponse,
)

setup_dishka(container=container, app=app)

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)
