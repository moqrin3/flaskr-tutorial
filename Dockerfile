FROM python:3.5-slim

MAINTAINER moqrin3

USER root

RUN apt-get update
RUN apt-get -qq -y install gcc python-dev default-libmysqlclient-dev mysql-client

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN chmod +x docker-entrypoint.sh
EXPOSE 80

ENTRYPOINT ["./docker-entrypoint.sh"]