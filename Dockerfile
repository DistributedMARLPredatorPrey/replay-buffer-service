FROM python:3.11

WORKDIR /usr/app

COPY . .
RUN pip install .

EXPOSE 80

CMD [ "gunicorn", "--threads", "1", "-b", "0.0.0.0:80", "src.main.run_server:app()" ]
