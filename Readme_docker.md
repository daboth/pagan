# using pagan and docker

## pagan webserver

Running pagan webserver on port 8080.

### Build:

docker build -t paganweb -f Dockerfile.webserver .

### Run:

docker run -d -p 8080:8080 paganweb

or:

docker run --rm -p 8080:8080 paganweb

### Stop:

docker stop <ID>

### Debug:

docker exec -it <ID> bash

### Docker ID:

docker ps
