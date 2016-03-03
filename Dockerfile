FROM ubuntu

MAINTAINER Matt Kantor <matt@propellerhead.ca>

RUN apt-get update -y && apt-get install git python python-pip -y
RUN cd /tmp \
    && git clone https://github.com/propellerhead-interactive/cbc-analytics-server.git \
    && cd cbc-analytics-server \
    && pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "/tmp/cbc-analytics-server/tserver.py"]