from dishka import make_async_container
from dishka.integrations import fastapi as dishka_fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from pocket_kai.config import Settings, get_settings
from pocket_kai.controllers.http.routers.main import router
from pocket_kai.ioc.main import providers


tags_metadata = [
    {
        'name': 'Groups',
        'description': (
            'Эндпоинты для работы с группы. '
            'Также есть отдельные категории связанные с группами: `Groups schedule`'
        ),
    },
    {
        'name': 'Groups schedule',
        'description': 'Эндпоинты для работы с расписанием групп',
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
]

description = """
Pocket KAI API

## Сервисные токены
Сервисные токены нужны для доступа к **служебным** эндпоинтам. Такие токены выпускаются только админами.

## Занятия
**Parsed dates status** - Статус спаршенных дат. Может быть `good` или `need_check`.
`good` - даты получилось распарсить точно, таким датам можно доверять. `need_check` - даты либо не получилось распарсить; либо получилось, но неточно;
либо даты разделены на подгруппы. Такие даты конечному пользователю следует перепроверить самому.


**! Даты распаршиваются в `parsed_dates` и `parsed_parity` !**
"""

settings = get_settings()
container = make_async_container(
    *providers,
    context={Settings: settings},
)

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
]


def get_fastapi_app(lifespan=None) -> FastAPI:
    app = FastAPI(
        title='Pocket KAI API',
        description=description,
        openapi_tags=tags_metadata,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


def get_production_fastapi_app() -> FastAPI:
    fastapi_app = get_fastapi_app()

    Instrumentator().instrument(fastapi_app).expose(fastapi_app)

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    dishka_fastapi.setup_dishka(container=container, app=fastapi_app)

    return fastapi_app
