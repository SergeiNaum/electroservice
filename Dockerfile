FROM python:3.10.3

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN mkdir -p /app
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . .

RUN chmod -R 777 ./