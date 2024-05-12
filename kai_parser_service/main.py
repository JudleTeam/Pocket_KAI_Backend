import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

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
