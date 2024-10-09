FROM python:3.8-slim-buster

WORKDIR /app

ADD requirements.txt /app/

RUN python -m pip install -r requirements.txt

ADD ./app /app/app

ENV PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--log-config", "app/config/logging.conf"]