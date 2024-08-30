FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

CMD ["bash"]

RUN apt-get update
RUN apt-get install -y python3 python3-pip git ca-certificates lsb-release ubuntu-keyring software-properties-common
RUN update-ca-certificates --fresh
RUN export SSL_CERT_DIR=/etc/ssl/certs
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN apt install -y tesseract-ocr
RUN apt install -y libtesseract-dev
RUN apt install -y poppler-utils

COPY ./requirements /ragger/requirements
WORKDIR /ragger
RUN pip install -r requirements/test.txt
RUN python3 -m spacy download en_core_web_sm
COPY . /ragger
RUN touch logs.log

RUN export GIT_PYTHON_GIT_EXECUTABLE=$(which git)
