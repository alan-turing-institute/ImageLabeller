FROM ubuntu:16.04 as imlabel_base

### get pip git etc

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install python-pip
RUN apt-get update; apt-get -y install python3-psycopg2

####### install python packages for the frontend
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install  flask
RUN pip3 install  flask_cors
RUN pip3 install  flask_session
RUN pip3 install  flask_bootstrap
RUN pip3 install  flask_login
RUN pip3 install  flask_sqlalchemy
RUN pip3 install  flask_wtf
RUN pip3 install  wtforms
RUN pip3 install  pytest
RUN pip3 install  sqlalchemy
RUN pip3 install requests
RUN pip3 install psycopg2-binary

#### environment variables for database

ENV DB_TYPE postgres
ENV DB_USER postgres
ENV DB_PASSWORD il
ENV DB_DATABASE img-labeller
ENV DB_HOST postgres
ENV DB_PORT 5432


#### run the flask app

ADD . /webapp

#
WORKDIR /webapp
####
EXPOSE 5000
ENV FLASK_APP il_app.py
####
CMD ["python3","il_app.py"]
