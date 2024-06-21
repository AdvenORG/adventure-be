FROM python:3.11.3


WORKDIR /server

RUN pip install poetry==1.8.1

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root --no-directory

COPY . .

RUN poetry install --no-interaction --no-ansi


EXPOSE 8000


CMD  make start_container