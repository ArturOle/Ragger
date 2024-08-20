FROM ubuntu:20.04

RUN useradd --create-home myuser
USER myuser
CMD ["bash"]

RUN apt-get update && apt-get install -y python3.11
COPY ./requirements/base.txt /ragger/requirements/base.txt
WORKDIR /ragger
RUN pip install -r requirements/base.txt

COPY . /ragger