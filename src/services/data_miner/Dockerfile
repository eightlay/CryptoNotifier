FROM python:3.11-slim

RUN useradd -ms /bin/bash data_miner
USER data_miner
WORKDIR /home/data_miner

COPY ./services/data_miner/requirements.txt requirements.txt

USER root
RUN apt-get update \
    && pip3 install -r requirements.txt
USER data_miner

COPY ./services/data_miner/app /home/data_miner
COPY ./shared_modules /home/data_miner/shared_modules

CMD [ "python3", "main.py"]
