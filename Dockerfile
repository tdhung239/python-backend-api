FROM python:3.8.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN apt-get install default-libmysqlclient-dev
RUN pip install mysqlclient
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . ./