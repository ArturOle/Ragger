FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

CMD ["bash"]

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt install -y tesseract-ocr
RUN apt install -y libtesseract-dev
RUN apt install -y poppler-utils

COPY ./requirements /ragger/requirements
WORKDIR /ragger
RUN pip install -r requirements/test.txt
COPY . /ragger
RUN touch logs.log
