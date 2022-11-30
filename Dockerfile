from python:3.11

RUN apt-get update

# Installing dependencies
RUN apt-get install -y \
    python-setuptools \
    openssh-server \
    openssh-client \
    x11-xserver-utils \
    sudo
RUN pip install Pillow bottle

# Adding pagan user in order to be able to connect through ssh (user: pagan, pass: pagan)
RUN useradd -m pagan && echo "pagan:pagan" | chpasswd && adduser pagan sudo


# Copying files
COPY . .

# Installing pagan
RUN python3 setup.py install

# Exposing port
EXPOSE 8080

#Starting ssh server and webserver app
CMD service ssh start && python3 tools/webserver/webserver.py
