from python:2.7

RUN apt-get update
RUN pip install bottle
RUN apt-get install -y \
    python-setuptools \
    python-imaging \
    openssh-server \
    openssh-client \
    x11-xserver-utils \
    sudo

RUN useradd -m pagan && echo "pagan:pagan" | chpasswd && adduser pagan sudo


COPY . .

RUN python setup.py install

EXPOSE 8080

CMD service ssh start && python tools/webserver/webserver.py