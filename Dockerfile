FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "pip>=23.0.0" setuptools wheel

COPY . .

RUN pip install -e .

FROM base AS web

CMD ["uvicorn", "teawish.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS migrations

CMD ["alembic", "upgrade", "head"]
