# Use official Python image
# FROM python:3.11-slim
FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy app code
COPY app /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

EXPOSE 9080

ENV PYTHONUNBUFFERED=1


# Run the app
# CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD uv run fastapi --verbose dev main.py
CMD uvx uvicorn main:app --proxy-headers --host 0.0.0.0 --port 9181 --reload
