FROM python:3.12.6-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.2.1"

RUN poetry config virtualenvs.create false

COPY certs/ ./certs/
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY src/ ./src/

CMD ["python", "-m", "src.app"]
