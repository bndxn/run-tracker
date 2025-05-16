FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-ansi --no-interaction

COPY src/ ./src/

ENV PYTHONPATH=/var/task/src
ENV HOME=/tmp

CMD ["src.fetch_and_suggest.main.lambda_handler"]
