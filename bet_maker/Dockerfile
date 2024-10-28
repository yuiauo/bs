FROM python:3.10.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /bet_maker
RUN pip install poetry==1.8.4
COPY poetry.lock pyproject.toml /bet_maker/
RUN apt-get update \
 && apt-get -y install libpq-dev gcc
RUN poetry config virtualenvs.create false \
 && poetry install

# Creating folders, and files for a project:
COPY . /bet_maker
EXPOSE 8081
