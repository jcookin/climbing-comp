FROM python:3.12-alpine3.20

# Cache the pip upgrade before any copies
RUN pip install --upgrade pip

USER 1000

WORKDIR /app

COPY requirements.txt .

USER 0
RUN pip install -r requirements.txt
USER 1000

COPY src/ .

EXPOSE 8000

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0", "app:app" ]
