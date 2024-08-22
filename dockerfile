FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

CMD ["bash"]

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt install -y tesseract-ocr
RUN apt install -y libtesseract-dev
RUN apt install -y poppler-utils

RUN useradd --create-home myuser

COPY ./requirements/base.txt /ragger/requirements/base.txt
WORKDIR /ragger
RUN pip install -r requirements/base.txt

COPY . /ragger

RUN touch logs.log
RUN chown -R myuser:myuser /ragger && chmod -R 755 /ragger && chmod -R 755 /ragger/logs.log
