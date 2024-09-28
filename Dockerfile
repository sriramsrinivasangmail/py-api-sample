FROM quay.io/ibm_cpd_zen/zen-python:latest

## can't develop without vim
RUN apt-get update && apt install -y vim

## install dependencies first to improve cachability of this layer
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY app  /app

ENTRYPOINT ["/app/src/main.py"]
ENV HOME /tmp
USER 1001
