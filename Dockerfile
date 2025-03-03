FROM python:3.12-alpine3.20

USER 1000

WORKDIR /app

COPY requirements.txt .
COPY src/ .

ENTRYPOINT [ "gunicorn", "-w", "4", "app:app" ]
