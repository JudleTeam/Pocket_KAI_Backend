FROM python:3.11-slim
LABEL authors="printeromg"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml .
RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

WORKDIR /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]