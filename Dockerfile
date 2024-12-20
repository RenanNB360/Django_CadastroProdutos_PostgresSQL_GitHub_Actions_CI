FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . /app/
COPY entrypoint.sh /app/entrypoint.sh
RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install poetry

RUN poetry install --with dev --no-interaction --no-ansi

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080
CMD ["./entrypoint.sh"]