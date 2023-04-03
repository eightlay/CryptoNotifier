FROM python:3.11-slim

RUN useradd -ms /bin/bash researcher
USER researcher
WORKDIR /home/researcher

COPY ./services/researcher/requirements.txt requirements.txt

USER root
RUN apt-get update \
    && pip3 install -r requirements.txt
USER researcher

COPY ./services/researcher/app /home/researcher
COPY ./shared_modules /home/researcher/shared_modules

CMD [ "python3", "main.py"]
