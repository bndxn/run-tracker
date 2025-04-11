FROM python:3.12-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install poetry and project dependencies
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application source code
COPY src/ ./src/

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app/src

EXPOSE 80

# Run application
RUN poetry run python src/setup_config.py

CMD ["poetry", "run", "python", "src/web_app.py"]
