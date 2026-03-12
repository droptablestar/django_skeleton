FROM python:3.12-slim

# System deps required to build mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY . .

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
