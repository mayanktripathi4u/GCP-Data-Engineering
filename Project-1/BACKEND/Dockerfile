FROM python:3-slim

WORKDIR /app

COPY . /app

COPY config/serviceAccountKey.json /app/config/dev/serviceAccountKey.json

RUN pip install --cache-dir=/app/.pip_cache -r requirements.txt

EXPOSE 8080

ENV PORT=8080

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/config/dev/serviceAccountKey.json"

CMD [ "python3", "w", app.py ]

 