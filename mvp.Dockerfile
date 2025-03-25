FROM python:3.12-slim

WORKDIR /app

RUN pip install uv
COPY pyproject.toml ./

# Install dependencies using uv (best practice)
RUN uv venv && \
    uv pip install --system ".[all]"

# Copy the application source
COPY src/ ./src/
ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "python3 src/setup_config.py && python3 src/main.py"]
