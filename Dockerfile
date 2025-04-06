FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry

RUN poetry install

COPY . .

EXPOSE 8050

CMD ["poetry", "run", "gunicorn", "-w", "3", "-b", "0.0.0.0:8050", "app:server"]
