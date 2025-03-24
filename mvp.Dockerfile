FROM python:3.12-slim

# COPY src/ /app/src
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENV PYTHONPATH=/app/src

CMD ["poetry", "run", "sh", "-c", "python3 src/setup_config.py && python3 src/main.py"]
