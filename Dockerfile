from python:2.7

RUN apt-get update
RUN pip install bottle
RUN apt-get install -y \
    python-setuptools \
    python-imaging

COPY . .

RUN python setup.py install

EXPOSE 8080

CMD python tools/webserver/webserver.py