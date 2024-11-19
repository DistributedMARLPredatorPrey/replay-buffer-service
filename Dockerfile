FROM python:3.11

WORKDIR /usr/app

COPY . .
RUN pip install .

CMD ["sh", "-c", "gunicorn --threads 1 -b 0.0.0.0:$REPLAY_BUFFER_PORT src.main.run_server:app"]