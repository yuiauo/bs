FROM python:3.10.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /line_provider
RUN pip install poetry==1.8.4
COPY poetry.lock pyproject.toml /line_provider/
RUN poetry config virtualenvs.create false \
 && poetry install

COPY . /line_provider
EXPOSE 8080