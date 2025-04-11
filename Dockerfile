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
RUN "python src/setup_config.py"


CMD ["sh", "-c", "python src/setup_config.py && python src/web_app.py"]
