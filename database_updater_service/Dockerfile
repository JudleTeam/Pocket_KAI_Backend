FROM python:3.12-slim
LABEL authors="printeromg"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml .
RUN poetry install --no-root --no-dev

WORKDIR /app/

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]