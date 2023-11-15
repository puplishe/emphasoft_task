FROM python:3.10-slim

WORKDIR /emphasoft_task

ADD ./ /emphasoft_task/

RUN apt-get update \
    && apt-get -y install libpq-dev python-dev-is-python3 gcc

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python hotel/manage.py makemigrations && python hotel/manage.py migrate && python hotel/manage.py loaddata hotel/fixtures.json && python hotel/manage.py runserver 0.0.0.0:8000
