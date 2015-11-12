FROM python:2.7.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y ifstat 

EXPOSE 3000

CMD [ "python","application.py"]
