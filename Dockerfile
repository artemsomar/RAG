FROM python:3.12.6-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.2.1"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY certs/ ./certs/
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY src/ ./src/
COPY prestart.sh .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
CMD ["python", "-m", "src.app"]
