FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get -y install vim build-essential
RUN python3 -m pip install uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml .
COPY uv.lock* .

# Install dependencies
RUN uv sync

# Copy source code
COPY src/ ./src/

CMD ["uv", "run", "src/entrypoint.py"]
