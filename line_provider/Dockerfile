FROM python:3.10.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /line_provider
RUN pip install poetry==1.8.4
run ls
COPY ../poetry.lock ../pyproject.toml /line_provider/
RUN apt-get update \
 && apt-get -y install libpq-dev gcc \
 && poetry config virtualenvs.create false \
 && poetry install

# Creating folders, and files for a project:
COPY . /line_provider
EXPOSE 8081
